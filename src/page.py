import os
import re

from utils import markdown_to_html_node


def extract_title(markdown: str):
    heading_match = re.match(r"^# (.*)", markdown)
    if not heading_match:
        raise ValueError("No top-level heading found in the markdown content.")
    return heading_match.group(1).strip()


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(
        f"Generating page from {from_path} using template {template_path} to {dest_path}"
    )
    markdown_content = template_content = ""
    with open(from_path, "r") as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()

    html = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    final_content = template_content.replace("{{ Content }}", html).replace(
        "{{ Title }}", title
    )

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        _ = f.write(final_content)
    print(f"Page generated at {dest_path}")


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, relative_path[:-3] + ".html")
                generate_page(from_path, template_path, dest_path)
