# Pure Python command-line RSS reader

## Assumptions
RSS reader for receiving news from link, cashing it, saving to html/pdf and printing to stdout in simple or json format.

## Requirements

Do not need any additional installations for using as a script.

For using as a package please run first `pip install -r requirements.txt`

## Usage

To run the reader it's possible to assign either
`python rss_reader.py "RSS URL" [optional arguments]`

or  `rss_reader "RSS URL" [optional arguments]` (after installation)

```
usage: rss_reader [-h] [--version] [--limit LIMIT] [--json] [--verbose] [--colorize] [--date DATE] 
[--to-pdf TO_PDF] [--to-html TO_HTML] [source]
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