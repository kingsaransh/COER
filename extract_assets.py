#!/usr/bin/env python3
"""
Script to extract CSS and JavaScript from HTML files and create separate files.
Uses BeautifulSoup for proper HTML parsing.
"""
import os
from pathlib import Path
from bs4 import BeautifulSoup

def extract_assets(html_file_path):
    """Extract CSS and JS from HTML file and create separate files."""
    
    print(f"\nProcessing {html_file_path}...")
    
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get base name for output files
    base_name = Path(html_file_path).stem
    
    # Extract CSS from <style> tags
    css_content = []
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            css_content.append(style_tag.string)
        style_tag.decompose()  # Remove the style tag from HTML
    
    # Extract JavaScript from <script> tags (only inline scripts, not external)
    js_content = []
    for script_tag in soup.find_all('script'):
        # Skip external scripts (those with src attribute)
        if script_tag.get('src'):
            continue
        if script_tag.string:
            js_content.append(script_tag.string)
        script_tag.decompose()  # Remove the script tag from HTML
    
    # Write CSS file
    css_file = f'{base_name}.css'
    with open(css_file, 'w', encoding='utf-8') as f:
        if css_content:
            f.write('\n\n/* ===== CSS Extracted from HTML ===== */\n\n')
            f.write('\n\n/* --- Style Block 1 --- */\n\n'.join(css_content))
        else:
            f.write('/* CSS extracted from HTML */\n')
    print(f"  Created {css_file}")
    
    # Write JS file
    js_file = f'{base_name}.js'
    with open(js_file, 'w', encoding='utf-8') as f:
        if js_content:
            f.write('// ===== JavaScript Extracted from HTML =====\n\n')
            f.write('\n\n// --- Script Block ---\n\n'.join(js_content))
        else:
            f.write('// JavaScript extracted from HTML\n')
    print(f"  Created {js_file}")
    
    # Add CSS link in <head>
    if css_content:
        css_link = soup.new_tag('link', rel='stylesheet', type='text/css', href=f'{base_name}.css')
        head = soup.find('head')
        if head:
            # Insert after title or at the beginning
            title = head.find('title')
            if title:
                title.insert_after(css_link)
            else:
                head.insert(0, css_link)
        else:
            # Create head if it doesn't exist
            head = soup.new_tag('head')
            soup.html.insert(0, head)
            head.append(css_link)
    
    # Add JS script before </body>
    if js_content:
        js_script = soup.new_tag('script', src=f'{base_name}.js')
        body = soup.find('body')
        if body:
            body.append(js_script)
        else:
            # If no body, append to html
            soup.html.append(js_script)
    
    # Write updated HTML
    new_html_file = f'{base_name}.html'
    with open(new_html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"  Updated {new_html_file}")
    
    return css_file, js_file, new_html_file

if __name__ == '__main__':
    # Process all HTML files
    html_files = ['Index.html', 'dashboard.html', 'Profile.html']
    
    for html_file in html_files:
        if os.path.exists(html_file):
            extract_assets(html_file)
        else:
            print(f"  Warning: {html_file} not found, skipping...")
    
    print("\nExtraction complete!")
