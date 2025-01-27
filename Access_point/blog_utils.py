# my_app/blog_utils.py
import os
import markdown ## Used to help with links


BLOG_POSTS_DIR = "Access_point/blog_posts"

def load_blog_post(slug):
    """Loads a blog post by its slug."""
    # Ensure os is imported if not already

    # Construct the full path to the post directory
    post_dir = os.path.join(BLOG_POSTS_DIR, slug)
    print(f"Loading blog post for slug: {slug}, Full path: {post_dir}")

    if not os.path.isdir(post_dir):
        print(f"Directory does not exist: {post_dir}")
        return None  # Return None if the directory doesn't exist

    # Read metadata
    metadata_file = os.path.join(post_dir, "metadata.txt")
    if not os.path.exists(metadata_file):
        print(f"Metadata file missing: {metadata_file}")
        return None  # Return None if metadata.txt doesn't exist

    metadata = {}
    with open(metadata_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                key, value = line.strip().split(": ", 1)
                metadata[key] = value
            except ValueError:
                print(f"Error parsing metadata line: {line}")
                continue

    # Read content
    content_file = os.path.join(post_dir, "content.txt")
    if not os.path.exists(content_file):
        print(f"Content file missing: {content_file}")
        return None  # Return None if content.txt doesn't exist

    with open(content_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse Markdown content into HTML - for links
    content_html = markdown.markdown(content)


    # Combine metadata and content
    metadata["content"] = content_html
    metadata["slug"] = slug  # Add slug to metadata for linking purposes
    return metadata
