
import json
import os
import re

# Extensive Mapping based on dracula.example.json and common VSCode keys
# Extensive Mapping based on dracula.example.json and common VSCode keys
COLOR_MAPPING = {
    # Core Backgrounds
    "background": "editor.background",
    "editor.background": "editor.background",
    "editor.foreground": "editor.foreground",
    "elevated_surface.background": "editorWidget.background",
    "surface.background": "sideBar.background",
    "panel.background": "sideBar.background",
    "terminal.background": "terminal.background",
    
    # UI Elements
    "element.background": "input.background", # Better for inputs/lists
    "element.hover": "list.hoverBackground",
    "element.active": "list.activeSelectionBackground",
    "element.selected": "list.activeSelectionBackground",
    
    # Borders
    "border": "focusBorder",
    "border.variant": "sideBar.border",
    "border.focused": "focusBorder",
    "border.selected": "focusBorder",
    "border.disabled": "disabledForeground",
    
    # Text
    "text": "editor.foreground",
    "text.muted": "descriptionForeground",
    "text.placeholder": "input.placeholderForeground",
    "text.disabled": "disabledForeground",
    "text.accent": "textLink.foreground",
    
    # Icons
    "icon": "icon.foreground",
    "icon.muted": "foreground", # Fallback
    "icon.accent": "activityBarBadge.background",
    
    # Bars
    "status_bar.background": "statusBar.background",
    "title_bar.background": "titleBar.activeBackground",
    "title_bar.inactive_background": "titleBar.inactiveBackground",
    "tab_bar.background": "editorGroupHeader.tabsBackground",
    "toolbar.background": "breadcrumb.background",
    
    # Tabs
    "tab.active_background": "tab.activeBackground",
    "tab.inactive_background": "tab.inactiveBackground",
    
    # Editor
    "editor.active_line.background": "editor.lineHighlightBackground",
    "editor.highlighted_line.background": "editor.lineHighlightBackground",
    "editor.line_number": "editorLineNumber.foreground",
    "editor.active_line_number": "editorLineNumber.activeForeground",
    "editor.invisible": "editorWhitespace.foreground",
    "editor.wrap_guide": "editorIndentGuide.background",
    "editor.active_wrap_guide": "editorIndentGuide.activeBackground",
    "editor.indent_guide": "editorIndentGuide.background",
    "editor.indent_guide_active": "editorIndentGuide.activeBackground",
    
    # Search & Highlights
    "search.match_background": "editor.findMatchBackground",
    "editor.document_highlight.read_background": "editor.selectionBackground",
    "editor.document_highlight.write_background": "editor.selectionBackground",
    "editor.document_highlight.bracket_background": "editorBracketMatch.background",
    
    # Git
    "conflict": "gitDecoration.conflictingResourceForeground",
    "created": "gitDecoration.addedResourceForeground",
    "deleted": "gitDecoration.deletedResourceForeground",
    "modified": "gitDecoration.modifiedResourceForeground",
    "ignored": "gitDecoration.ignoredResourceForeground",
    "renamed": "gitDecoration.renamedResourceForeground",
    
    # Diagnostics
    "error": "editorError.foreground",
    "warning": "editorWarning.foreground",
    "info": "editorInfo.foreground",
    "hint": "editorHint.foreground",
    
    # Scrollbar
    "scrollbar.thumb.background": "scrollbarSlider.background",
    "scrollbar.thumb.hover_background": "scrollbarSlider.hoverBackground",
    "scrollbar.track.background": "editor.background", # Often transparent in VSCode
}

# Values that might need transparency or specific fallbacks
DEFAULT_COLORS = {
    "border": "#00000000",
    "editor.background": "#1e1e1e",
    "editor.foreground": "#d4d4d4",
}

# Syntax Mapping (VSCode Scope -> Zed Key)
# Zed keys based on local schema (dracula.example.json)
SYNTAX_MAPPING = {
    "comment": "comment",
    "string": "string",
    "string.regexp": "string.regex",
    "string.escape": "string.escape",
    
    "constant": "constant",
    "constant.numeric": "number",
    "constant.language": "boolean", # True/False/Null
    "constant.character.escape": "string.escape",
    "constant.charcter.escape": "string.escape", # Typo in some themes
    
    "keyword": "keyword",
    "keyword.control": "keyword",
    "keyword.operator": "operator",
    "storage": "keyword",
    "storage.type": "keyword",
    "storage.modifier": "keyword",
    
    "entity.name.type": "type",
    "entity.name.class": "type",
    "entity.name.function": "function",
    "entity.name.function.constructor": "constructor", # Specific Zed key for constructors
    
    "entity.name.section": "type",
    "entity.name.namespace": "type",
    
    # Prioritize specific tag name over generic tag
    "entity.name.tag": "tag",
    
    "entity.other.attribute-name": "attribute",
    
    "variable": ["variable", "property"],
    "variable.parameter": ["variable.parameter", "parameter"],
    "entity.name.variable.parameter": "variable.parameter",
    "variable.argument": ["variable.parameter", "parameter"], # VSCode often uses this for parameters
    
    "variable.language": "variable.special", # "this", "super", etc.
    "variable.other": "variable",
    "variable.other.property": "property",
    "support.type.property-name": "property",
    
    "punctuation": "punctuation",
    "punctuation.definition.tag": "punctuation",
    "punctuation.definition.string": "punctuation",
    "punctuation.separator.key-value": "punctuation",
    "punctuation.section": "punctuation.bracket", # Brackets/Braces
    "punctuation.terminator": "punctuation.delimiter", # Semicolons
    
    # Removing "meta.tag" to avoid overwriting specific tag colors
    "meta.function-call": "function",
    
    # Generic entity.name is often used for functions if entity.name.function is missing
    "entity.name": "function",
    
    "markup.bold": "emphasis.strong",
    "markup.italic": "emphasis",
}

ANSI_MAPPING = {
    "terminal.ansiBlack": "terminal.ansi.black",
    "terminal.ansiRed": "terminal.ansi.red",
    "terminal.ansiGreen": "terminal.ansi.green",
    "terminal.ansiYellow": "terminal.ansi.yellow",
    "terminal.ansiBlue": "terminal.ansi.blue",
    "terminal.ansiMagenta": "terminal.ansi.magenta",
    "terminal.ansiCyan": "terminal.ansi.cyan",
    "terminal.ansiWhite": "terminal.ansi.white",
    "terminal.ansiBrightBlack": "terminal.ansi.bright_black",
    "terminal.ansiBrightRed": "terminal.ansi.bright_red",
    "terminal.ansiBrightGreen": "terminal.ansi.bright_green",
    "terminal.ansiBrightYellow": "terminal.ansi.bright_yellow",
    "terminal.ansiBrightBlue": "terminal.ansi.bright_blue",
    "terminal.ansiBrightMagenta": "terminal.ansi.bright_magenta",
    "terminal.ansiBrightCyan": "terminal.ansi.bright_cyan",
    "terminal.ansiBrightWhite": "terminal.ansi.bright_white",
}

def remove_comments(json_str):
    # Matches strings (including escaped quotes) OR comments
    pattern = r'("(?:\\.|[^"\\])*")|//.*'
    def replace(match):
        # If it matched a string (group 1), keep it. Otherwise it's a comment, remove it.
        return match.group(1) or ""
    return re.sub(pattern, replace, json_str)

def load_json(path):
    with open(path, 'r') as f:
        content = f.read()
        try:
            # First try strict load (fast path for valid JSON like package.json)
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback for JSONC (comments, trailing commas)
            # Remove comments
            content = remove_comments(content)
            # Remove trailing commas (simple approach)
            content = re.sub(r',(\s*?[}\]])', r'\1', content)
            return json.loads(content)

def get_color(colors, key, fallback=None):
    val = colors.get(key)
    if val:
        return val
    return fallback

def convert_syntax(token_colors):
    syntax = {}
    
    # Sort token colors by specificy (naively, just process order)
    # Zed syntax is a flat dict of key -> {color, font_style}
    
    for token in token_colors:
        scope = token.get("scope")
        settings = token.get("settings", {})
        foreground = settings.get("foreground")
        font_style = settings.get("fontStyle")
        
        if not foreground and not font_style:
            continue
            
        if isinstance(scope, str):
            scopes = [scope]
        elif isinstance(scope, list):
            scopes = scope
        else:
            continue
            
        for s in scopes:
            # Find best match in SYNTAX_MAPPING
            best_match_val = None
            best_match_len = 0
            
            for vs_scope, zed_val in SYNTAX_MAPPING.items():
                if s == vs_scope or s.startswith(vs_scope + "."):
                    if len(vs_scope) > best_match_len:
                        best_match_len = len(vs_scope)
                        best_match_val = zed_val
            
            if best_match_val:
                # Handle list of Zed keys or single string
                if isinstance(best_match_val, list):
                    zed_keys = best_match_val
                else:
                    zed_keys = [best_match_val]
                
                for zed_key in zed_keys:
                    entry = {}
                    if foreground:
                        entry["color"] = foreground
                    if font_style:
                        entry["font_style"] = font_style
                        if "bold" in font_style:
                            entry["font_weight"] = 700
                        if "italic" in font_style:
                            entry["font_style"] = "italic"
                        else:
                            entry["font_style"] = None 
                            
                    if zed_key not in syntax:
                         syntax[zed_key] = entry
                         # Debug print
                         if zed_key == "property":
                             print(f"DEBUG: Mapped {s} to property with color {foreground}")
                    else:
                        # Update existing
                        syntax[zed_key].update(entry)

    return syntax

def main():
    package_path = "package.json"
    if not os.path.exists(package_path):
        print("package.json not found")
        return
        
    pkg = load_json(package_path)
    themes = pkg.get("contributes", {}).get("themes", [])
    
    os.makedirs("themes", exist_ok=True) # Output to "themes" dir as per user request
    
    for theme_entry in themes:
        label = theme_entry.get("label")
        path = theme_entry.get("path")
        ui_theme = theme_entry.get("uiTheme", "vs-dark")
        appearance = "light" if "light" in ui_theme else "dark"
        
        print(f"Processing {label}...")
        
        try:
            vs_data = load_json(path)
            colors = vs_data.get("colors", {})
            token_colors = vs_data.get("tokenColors", [])
            
            # Build Style
            style = {}
            
            # Map Colors
            for zed_key, vs_key in COLOR_MAPPING.items():
                if vs_key in colors:
                    style[zed_key] = colors[vs_key]
            
            # Map ANSI
            for vs_key, zed_key in ANSI_MAPPING.items():
                if vs_key in colors:
                    style[zed_key] = colors[vs_key]
            
            # Map Syntax
            style["syntax"] = convert_syntax(token_colors)
            
            # Players (Cursors)
            # Use accent color or default
            cursor_color = colors.get("editorCursor.foreground", "#FFFFFF")
            selection_color = colors.get("editor.selectionBackground", "#FFFFFF44")
            
            style["players"] = [
                {
                    "cursor": cursor_color,
                    "background": cursor_color,
                    "selection": selection_color
                }
            ]
            
            # Add implicit Accents if missing
            style["accents"] = [colors.get("activityBarBadge.background", "#FF0000")]
            
            # Construct Final Object
            zed_theme = {
                "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
                "name": label,
                "author": pkg.get("publisher", "Unknown"),
                "themes": [
                    {
                        "name": label,
                        "appearance": appearance,
                        "style": style
                    }
                ]
            }
            
            out_name = f"{label}.json"
            # Normalize filename
            out_name = out_name.replace(" ", "_")
            out_path = os.path.join("themes", out_name)
            
            with open(out_path, 'w') as f:
                json.dump(zed_theme, f, indent=2)
                
            print(f"  -> Generated {out_path}")
            
        except Exception as e:
            print(f"  -> Error converting {label}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
