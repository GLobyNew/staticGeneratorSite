from textnode import *
from htmlnode import *
from markdown_blocks import *
import os
import shutil


def prepare_copying():
    # Check if static exist
    if not os.path.exists("./static"):
        raise Exception("No 'static' folder inside path, nothing to generate")
    # Wipe public folder and create it again
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")


def copy_files_recursively(source_folder, dest_folder):
    files = os.listdir(source_folder)
    for file in files:
        path_to_file = os.path.join(source_folder, file)
        if os.path.isfile(path_to_file):
            shutil.copy(path_to_file, dest_folder)
        elif os.path.isdir(path_to_file):
            new_folder_path = os.path.join(dest_folder, file)
            os.mkdir(new_folder_path)
            copy_files_recursively(path_to_file, new_folder_path)
    


def extract_title(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        if block_to_block_type(block) == BlockType.HEADING and count_heading_level(block) == 1:
            return remove_heading_from_block(block, count_heading_level(block))
    raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generate page from {from_path} to {
          dest_path} using {template_path}")
    with open(from_path) as fr:
        md_content = fr.read()
    with open(template_path) as tp:
        template = tp.read()
    title = extract_title(md_content)
    content = markdown_to_html_node(md_content).to_html()
    rdy_doc = template.replace("{{ Title }}", title)
    rdy_doc = rdy_doc.replace("{{ Content }}", content)

    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as out:
        out.write(rdy_doc)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = os.listdir(dir_path_content)
    for file in files:
        path_to_file = os.path.join(dir_path_content, file)
        path_to_dest = os.path.join(dest_dir_path, file.replace(".md", ".html"))
        if os.path.isfile(path_to_file):
            generate_page(path_to_file, template_path, path_to_dest)
        elif os.path.isdir(path_to_file):
            new_folder_path = os.path.join(dest_dir_path, file)
            generate_pages_recursive(path_to_file, template_path, new_folder_path)


def main():
    prepare_copying()
    copy_files_recursively("./static", "./public/")
    generate_pages_recursive("./content/", "template.html", "./public/")


if __name__ == "__main__":
    main()
