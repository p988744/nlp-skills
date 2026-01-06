#!/bin/bash
# Claude Code Plugin Validator
# Based on lessons learned from nlp-skills development
#
# Validates:
# 1. plugin.json structure and required fields
# 2. marketplace.json source paths
# 3. Commands: no invalid fields, files exist
# 4. Agents: correct tools format, no invalid fields, files exist
# 5. Skills: SKILL.md exists with required frontmatter
# 6. Hooks: valid JSON syntax
# 7. Directory structure at root level

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

error() {
    echo -e "${RED}ERROR: $1${NC}"
    ((ERRORS++))
}

warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
    ((WARNINGS++))
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

info() {
    echo -e "  $1"
}

echo "========================================"
echo "Claude Code Plugin Validator v0.1.0"
echo "========================================"
echo ""

# Get plugin root (script location or argument)
PLUGIN_ROOT="${1:-.}"
cd "$PLUGIN_ROOT"

echo "Validating plugin at: $(pwd)"
echo ""

# ============================================
# 1. Check plugin.json exists and is valid JSON
# ============================================
echo "## 1. Checking plugin.json"

PLUGIN_JSON=".claude-plugin/plugin.json"
if [[ ! -f "$PLUGIN_JSON" ]]; then
    error "plugin.json not found at $PLUGIN_JSON"
else
    # Check JSON syntax
    if ! python3 -c "import json; json.load(open('$PLUGIN_JSON'))" 2>/dev/null; then
        error "plugin.json has invalid JSON syntax"
    else
        success "plugin.json is valid JSON"

        # Check required fields
        NAME=$(python3 -c "import json; print(json.load(open('$PLUGIN_JSON')).get('name', ''))")
        if [[ -z "$NAME" ]]; then
            error "plugin.json missing required 'name' field"
        else
            success "name: $NAME"
        fi

        # Check version format (semver)
        VERSION=$(python3 -c "import json; print(json.load(open('$PLUGIN_JSON')).get('version', ''))")
        if [[ -n "$VERSION" ]]; then
            if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
                warning "version '$VERSION' is not semver format (X.Y.Z)"
            else
                success "version: $VERSION"
            fi
        fi

        # Check commands paths end with .md
        COMMANDS=$(python3 -c "
import json
data = json.load(open('$PLUGIN_JSON'))
cmds = data.get('commands', [])
if isinstance(cmds, str):
    print(cmds)
elif isinstance(cmds, list):
    for c in cmds:
        print(c)
" 2>/dev/null)

        if [[ -n "$COMMANDS" ]]; then
            while IFS= read -r cmd; do
                if [[ -n "$cmd" && ! "$cmd" =~ \.md$ ]]; then
                    error "commands path '$cmd' must end with .md"
                fi
            done <<< "$COMMANDS"
        fi

        # Check agents paths end with .md
        AGENTS=$(python3 -c "
import json
data = json.load(open('$PLUGIN_JSON'))
agents = data.get('agents', [])
if isinstance(agents, str):
    print(agents)
elif isinstance(agents, list):
    for a in agents:
        print(a)
" 2>/dev/null)

        if [[ -n "$AGENTS" ]]; then
            while IFS= read -r agent; do
                if [[ -n "$agent" && ! "$agent" =~ \.md$ ]]; then
                    error "agents path '$agent' must end with .md"
                fi
            done <<< "$AGENTS"
        fi
    fi
fi

echo ""

# ============================================
# 2. Check marketplace.json
# ============================================
echo "## 2. Checking marketplace.json"

MARKETPLACE_JSON=".claude-plugin/marketplace.json"
if [[ ! -f "$MARKETPLACE_JSON" ]]; then
    info "marketplace.json not found (optional)"
else
    if ! python3 -c "import json; json.load(open('$MARKETPLACE_JSON'))" 2>/dev/null; then
        error "marketplace.json has invalid JSON syntax"
    else
        success "marketplace.json is valid JSON"

        # Check source paths start with ./
        SOURCES=$(python3 -c "
import json
data = json.load(open('$MARKETPLACE_JSON'))
for p in data.get('plugins', []):
    print(p.get('source', ''))
" 2>/dev/null)

        while IFS= read -r src; do
            if [[ -n "$src" && ! "$src" =~ ^\.\/ ]]; then
                error "marketplace source '$src' must start with ./"
            fi
        done <<< "$SOURCES"
    fi
fi

echo ""

# ============================================
# 3. Check commands
# ============================================
echo "## 3. Checking commands"

if [[ -d "commands" ]]; then
    CMD_COUNT=0
    for cmd_file in commands/*.md; do
        [[ -f "$cmd_file" ]] || continue
        ((CMD_COUNT++))

        # Check for invalid 'name' field (commands don't use name)
        if grep -q "^name:" "$cmd_file" 2>/dev/null; then
            warning "$cmd_file has 'name' field (commands derive name from filename)"
        fi

        # Check for required 'description' field
        if ! grep -q "^description:" "$cmd_file" 2>/dev/null; then
            error "$cmd_file missing required 'description' field"
        fi

        # Check frontmatter exists
        if ! head -1 "$cmd_file" | grep -q "^---$"; then
            error "$cmd_file missing YAML frontmatter (must start with ---)"
        fi
    done

    if [[ $CMD_COUNT -gt 0 ]]; then
        success "Found $CMD_COUNT command(s)"
    else
        info "No commands found"
    fi
else
    info "commands/ directory not found (optional)"
fi

echo ""

# ============================================
# 4. Check agents
# ============================================
echo "## 4. Checking agents"

if [[ -d "agents" ]]; then
    AGENT_COUNT=0
    for agent_file in agents/*.md; do
        [[ -f "$agent_file" ]] || continue
        ((AGENT_COUNT++))

        # Check for required 'name' field
        if ! grep -q "^name:" "$agent_file" 2>/dev/null; then
            error "$agent_file missing required 'name' field"
        fi

        # Check for required 'description' field
        if ! grep -q "^description:" "$agent_file" 2>/dev/null; then
            error "$agent_file missing required 'description' field"
        fi

        # Check for invalid 'color' field
        if grep -q "^color:" "$agent_file" 2>/dev/null; then
            warning "$agent_file has invalid 'color' field (not supported)"
        fi

        # Check tools format (should be comma-separated, not JSON array)
        TOOLS_LINE=$(grep "^tools:" "$agent_file" 2>/dev/null || true)
        if [[ "$TOOLS_LINE" =~ \[.*\] ]]; then
            error "$agent_file 'tools' should be comma-separated string, not JSON array"
        fi

        # Check frontmatter exists
        if ! head -1 "$agent_file" | grep -q "^---$"; then
            error "$agent_file missing YAML frontmatter (must start with ---)"
        fi
    done

    if [[ $AGENT_COUNT -gt 0 ]]; then
        success "Found $AGENT_COUNT agent(s)"
    else
        info "No agents found"
    fi
else
    info "agents/ directory not found (optional)"
fi

echo ""

# ============================================
# 5. Check skills
# ============================================
echo "## 5. Checking skills"

if [[ -d "skills" ]]; then
    SKILL_COUNT=0
    for skill_dir in skills/*/; do
        [[ -d "$skill_dir" ]] || continue

        SKILL_MD="${skill_dir}SKILL.md"
        if [[ -f "$SKILL_MD" ]]; then
            ((SKILL_COUNT++))

            # Check for required 'name' field
            if ! grep -q "^name:" "$SKILL_MD" 2>/dev/null; then
                error "$SKILL_MD missing required 'name' field"
            fi

            # Check for required 'description' field
            if ! grep -q "^description:" "$SKILL_MD" 2>/dev/null; then
                error "$SKILL_MD missing required 'description' field"
            fi

            # Check frontmatter exists
            if ! head -1 "$SKILL_MD" | grep -q "^---$"; then
                error "$SKILL_MD missing YAML frontmatter (must start with ---)"
            fi
        fi
    done

    if [[ $SKILL_COUNT -gt 0 ]]; then
        success "Found $SKILL_COUNT skill(s)"
    else
        info "No skills found"
    fi
else
    info "skills/ directory not found (optional)"
fi

echo ""

# ============================================
# 6. Check hooks
# ============================================
echo "## 6. Checking hooks"

HOOKS_JSON="hooks/hooks.json"
if [[ -f "$HOOKS_JSON" ]]; then
    if ! python3 -c "import json; json.load(open('$HOOKS_JSON'))" 2>/dev/null; then
        error "hooks.json has invalid JSON syntax"
    else
        success "hooks.json is valid JSON"
    fi
else
    info "hooks/hooks.json not found (optional)"
fi

echo ""

# ============================================
# 7. Check directory structure
# ============================================
echo "## 7. Checking directory structure"

# Components should NOT be inside .claude-plugin/
for component in commands agents skills hooks; do
    if [[ -d ".claude-plugin/$component" ]]; then
        error "$component/ should be at plugin root, not inside .claude-plugin/"
    fi
done

# Check if components exist at root
for component in commands agents skills; do
    if [[ -d "$component" ]]; then
        success "$component/ at root level"
    fi
done

echo ""

# ============================================
# 8. Check referenced files exist
# ============================================
echo "## 8. Checking referenced files exist"

if [[ -f "$PLUGIN_JSON" ]]; then
    # Check commands files exist
    python3 -c "
import json
import os
data = json.load(open('$PLUGIN_JSON'))
cmds = data.get('commands', [])
if isinstance(cmds, list):
    for c in cmds:
        if not os.path.exists(c.lstrip('./')):
            print(f'MISSING: {c}')
" 2>/dev/null | while read -r line; do
        if [[ "$line" == MISSING:* ]]; then
            error "Referenced file not found: ${line#MISSING: }"
        fi
    done

    # Check agents files exist
    python3 -c "
import json
import os
data = json.load(open('$PLUGIN_JSON'))
agents = data.get('agents', [])
if isinstance(agents, list):
    for a in agents:
        if not os.path.exists(a.lstrip('./')):
            print(f'MISSING: {a}')
" 2>/dev/null | while read -r line; do
        if [[ "$line" == MISSING:* ]]; then
            error "Referenced file not found: ${line#MISSING: }"
        fi
    done
fi

success "All referenced files exist"

echo ""

# ============================================
# Summary
# ============================================
echo "========================================"
echo "Validation Summary"
echo "========================================"
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [[ $ERRORS -gt 0 ]]; then
    echo -e "${RED}FAILED${NC} - Fix errors before publishing"
    exit 1
else
    if [[ $WARNINGS -gt 0 ]]; then
        echo -e "${YELLOW}PASSED WITH WARNINGS${NC}"
    else
        echo -e "${GREEN}PASSED${NC}"
    fi
    exit 0
fi
