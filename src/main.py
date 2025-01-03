from static_copy import static_refresh
from markdown import generate_page, generate_pages_recursive

def main():

	static_refresh()
	generate_pages_recursive("content", "template.html", "public")
	
main()
