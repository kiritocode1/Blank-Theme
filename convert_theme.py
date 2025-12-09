
import json
import os
import re

# VSCode to Zed Mapping
# This is a best-effort mapping based on common keys.
COLOR_MAPPING = {
    # Core UI
    "editor.background": "editor.background",
    "editor.foreground": "editor.foreground",
    "activityBar.background": "tab_bar.background", # Approximate
    "sideBar.background": "panel.background",
    "statusBar.background": "status_bar.background",
    "titleBar.activeBackground": "title_bar.background",
    "terminal.background": "terminal.background",
    
    # Borders
    "focusBorder": "border.focused",
    "sideBar.border": "border",
    "statusBar.border": "border",
    "activityBar.border": "border",
    "titleBar.border": "border",
    
    # Text
    "foreground": "text.primary",
    "descriptionForeground": "text.muted",
    "errorForeground": "text.error",
    
    # Git
    "gitDecoration.addedResourceForeground": "git.created",
    "gitDecoration.modifiedResourceForeground": "git.modified",
    "gitDecoration.deletedResourceForeground": "git.deleted",
    "gitDecoration.conflictingResourceForeground": "git.conflict",
    "gitDecoration.ignoredResourceForeground": "git.ignored",

    # Editor Syntax (approximate, Zed uses specific syntax keys)
    # We will try to map tokenColors separately
}

# Zed Syntax Scopes Mapping 
# VSCode TextMate scopes -> Zed syntax keys
# Source: https://zed.dev/docs/themes#syntax-colors
SYNTAX_MAPPING = {
    "comment": "comment",
    "string": "string",
    "constant.numeric": "constant",
    "constant.language": "constant",
    "keyword": "keyword",
    "storage": "keyword",
    "entity.name.function": "function",
    "support.function": "function",
    "entity.name.type": "type",
    "support.class": "type",
    "variable": "variable",
    "variable.parameter": "property", # Close enough
    "entity.name.tag": "tag",
    "entity.other.attribute-name": "attribute",
}

def load_json(path):
    with open(path, 'r') as f:
        content = f.read()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to strip comments if standard load fails
            # This regex is still simple but avoids http://
            # It looks for // that is NOT preceded by :
            # But better: just use a known robust pattern or rely on lines.
            lines = content.split('\n')
            clean_lines = []
            for line in lines:
                if '//' in line:
                    # Simple check: if // follows "http:" or "https:", don't strip.
                    # This is a hack but works for this context.
                    if "http://" in line or "https://" in line:
                        clean_lines.append(line)
                        continue
                        
                    parts = line.split('//')
                    clean_lines.append(parts[0])
                else:
                    clean_lines.append(line)
            return json.loads('\n'.join(clean_lines))

def convert_color(hex_color):
    # Ensure it's a string
    if not isinstance(hex_color, str):
        return None
    # VSCode handles #RRGGBBAA, Zed also supports it.
    return hex_color

def map_theme(vscode_theme, theme_name):
    zed_theme = {
        "name": theme_name,
        "author": "kiritocode1",
        "themes": [
            {
                "name": theme_name,
                "appearance": "dark", # Assuming dark from package.json
                "style": {
                    "border": vscode_theme.get("colors", {}).get("focusBorder", "#817c9c26"), # Fallback
                     "players": [
                        {
                            "cursor": vscode_theme.get("colors", {}).get("editorCursor.foreground", "#c58fff"),
                            "selection": vscode_theme.get("colors", {}).get("editor.selectionBackground", "#817c9c26")
                        }
                    ],
                    "syntax": {},
                }
            }
        ]
    }
    
    style = zed_theme["themes"][0]["style"]
    colors = vscode_theme.get("colors", {})
    
    # 1. Map Core Colors
    # Zed structure is flatter for some things, nested for others.
    # We'll construct a basic palette.
    
    # Backgrounds
    style["background"] = colors.get("editor.background", "#000000")
    style["editor.background"] = colors.get("editor.background", "#000000")
    style["panel.background"] = colors.get("sideBar.background", "#000000")
    style["status_bar.background"] = colors.get("statusBar.background", "#000000")
    style["title_bar.background"] = colors.get("titleBar.activeBackground", "#000000")
    style["terminal.background"] = colors.get("terminal.background", "#000000")

    # Foreground / Text
    style["text.primary"] = colors.get("foreground", "#868690")
    style["text.muted"] = colors.get("descriptionForeground", "#575861")
    
    # Accents & UI
    style["link_text.hover"] = colors.get("textLink.activeForeground", "#fdfdfe")
    
    # Git
    style["git.created"] = colors.get("gitDecoration.addedResourceForeground", "#c58fff")
    style["git.modified"] = colors.get("gitDecoration.modifiedResourceForeground", "#ffbb88")
    style["git.deleted"] = colors.get("gitDecoration.deletedResourceForeground", "#575861")

    # 2. Map Syntax
    # Zed syntax is in "syntax" key
    syntax = style["syntax"]
    token_colors = vscode_theme.get("tokenColors", [])
    
    for token in token_colors:
        scope = token.get("scope")
        settings = token.get("settings", {})
        foreground = settings.get("foreground")
        
        if not foreground:
            continue
            
        if isinstance(scope, str):
            scopes = [scope]
        elif isinstance(scope, list):
            scopes = scope
        else:
            continue
            
        for s in scopes:
            # Simple exact match or prefix match could be complex.
            # We check our mapping table.
            for vs_scope, zed_key in SYNTAX_MAPPING.items():
                if s.startswith(vs_scope):
                    syntax[zed_key] = {"color": foreground, "font_style": settings.get("fontStyle", None)}

    # Terminal Colors (Ansi)
    # Zed expects "terminal.ansi.X" in style? Or specific terminal block?
    # Checking schema: "terminal": { "black": ..., "red": ... } inside style seems valid or flattened.
    # Let's use flat keys as per recent Zed themes often seen.
    
    ansi_map = {
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
    
    for vs_key, zed_key in ansi_map.items():
        if vs_key in colors:
            style[zed_key] = colors[vs_key]

    return zed_theme

def main():
    package_json_path = "package.json"
    if not os.path.exists(package_json_path):
        print("package.json not found!")
        return

    pkg = load_json(package_json_path)
    
    output_dir = "zed-themes"
    os.makedirs(output_dir, exist_ok=True)
    
    themes = pkg.get("contributes", {}).get("themes", [])
    
    for theme_entry in themes:
        label = theme_entry.get("label")
        path = theme_entry.get("path")
        
        if not label or not path:
            continue
            
        print(f"Converting {label}...")
        
        try:
            vs_theme = load_json(path)
            zed_theme = map_theme(vs_theme, label)
            
            output_filename = f"{label}.json"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w') as f:
                json.dump(zed_theme, f, indent=4)
                
            print(f"Created {output_path}")
            
        except Exception as e:
            print(f"Failed to convert {label}: {e}")

if __name__ == "__main__":
    main()
