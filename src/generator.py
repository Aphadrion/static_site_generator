from blockmarkdown import *
from pathlib import Path
from copystatic import *
import os

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if block.startswith("# "):
                return block[1:].strip()
    raise Exception("missing h1 heading")

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as from_file:
        markdown_content = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()
    title = extract_title(markdown_content)

    html = html.replace('href="/', f'href="{base_path}')
    html = html.replace('src="/', f'src="{base_path}')

    if "{{ Title }}" not in template or "{{ Content }}" not in template:
        raise Exception("Template is missing required placeholders: {{ Title }} or {{ Content }}")
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    os.makedirs(dest_dir_path, exist_ok=True)
    
    with open(dest_path, "w") as to_file:
        to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    content = os.listdir(dir_path_content)
    for item in content:
        source_path = os.path.join(dir_path_content,item)
        dest_file_path = os.path.join(dest_dir_path,item)

        if item.startswith("."):
            continue

        if os.path.isfile(source_path) and Path(source_path).suffix == '.md':
            dest_file_path = Path(dest_file_path).with_suffix(".html")
            print(f"Processing: {source_path}")
            generate_page(source_path, template_path, dest_file_path,base_path)
        elif os.path.isdir(source_path):
            os.makedirs(dest_file_path, exist_ok=True)
            generate_pages_recursive(source_path, template_path, dest_file_path,base_path)
       
#if __name__ == "__main__":
#    generate_page("content/index.md", "template.html", "public")