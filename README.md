Pure Python command-line RSS reader.

This rss_reader receives RSS URL and prints results in human-readable format.

Interface example:

    usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] 
                        source

    Pure Python command-line RSS reader

    positional arguments:
      source         RSS URL

    optional arguments:
      -h, --help        Show this help message and exit
      --version         Print version info
      --json            Print result as JSON in stdout
      --verbose         Outputs verbose status messages
      --limit LIMIT     Limit news topics if this parameter provided
      --date [DATE]     Get news on a specified date
      --to-html TO_HTML The absolute path where new .html file will be saved
      --to-pdf TO_PDF   The absolute path where new .pdf file will be saved
      --colorize        Prints the result of the utility in colorized mode

JSON structure:

    {
        article = {
                'Title': title,
                'Link': link,
                'Date': pubDate,
                'Source': source,
                'Image': imageLink,
        }
    }

Cache:

    Received news are stored in local sqlite3 database