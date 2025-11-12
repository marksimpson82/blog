"""
Quick and dirty script to manually specify the path for each (old) blog post to match
the old Jekyll URL scheme I'd chosen. My old posts had a URL scheme like the following:
/blog/YYYY/MM/DD/title-of-post.html
e.g. /blog/2008/11/08/assertthatpostcontent-textdoesnotcontainhello-world.html

Generates a toml path = "..." entry for each blog post

Sample text in original blog posts pre-path insertion:
+++
title = "Assert.That(post.Content, Text.DoesNotContain(\"Hello World\"));"
tags = ["misc"]
+++

We want to:
1. generate a path based on the format /blog/YYYY/MM/DD/title.html
2. poke it into the file content as frontmatter toml

example result for file 2008-11-08-assertthatpostcontent-textdoesnotcontainhello-world:
+++
title = "Assert.That(post.Content, Text.DoesNotContain(\"Hello World\"));"
tags = ["misc"]
path = "/blog/2008/11/08/assertthatpostcontent-textdoesnotcontainhello-world.html"
+++

I don't necessarily need to follow this url scheme for new posts. Might be easier to
just use the defaults for new posts.
"""

from pathlib import Path

def run(content_dir: Path, output_dir: Path):
    md_blog_files = list(content_dir.glob('**/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.md'))

    if not output_dir.exists():
        Path.mkdir(output_dir)
    
    for md_file in md_blog_files:
        yyyy = md_file.name[:4]
        mm = md_file.name[5:7]
        dd = md_file.name[8:10]
        rest_of_filename = md_file.name[11:-3]
                
        # format: "/blog/YYYY/MM/DD-rest-of-filename.html"
        derived_path = f"/blog/{yyyy}/{mm}/{dd}/{rest_of_filename}.html"
        path_text = 'path = \"' + derived_path + "\""

        with open(md_file, mode='r', encoding='utf-8') as source_file:
            md_file_text = source_file.read()
            last_toml_separator_index = md_file_text.rindex("+++")
            generated_text = md_file_text[:last_toml_separator_index] + path_text + "\n" + "+++" + md_file_text[last_toml_separator_index+3:]
        
            with open(Path.joinpath(output_dir, md_file.name), mode='w', encoding='utf-8') as dest_file:
                dest_file.write(generated_text)
        

if __name__ == "__main__":
    run(Path("./content/blog"), Path("C:/temp/processed"))