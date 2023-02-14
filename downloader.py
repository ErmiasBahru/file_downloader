from tqdm import tqdm
import requests
import cgi
import sys


url = sys.argv[1]
buffer_size = 1024
response = requests.get(url, stream=True)

# get the total file size
file_size = int(response.headers.get("Content-Length", 0))
# get the default filename
default_filename = url.split("/")[-1]

if content_disposition := response.headers.get("Content-Disposition"):
    value, params = cgi.parse_header(content_disposition)
    filename = params.get("filename", default_filename)
else:
    filename = default_filename

progress = tqdm(response.iter_content(buffer_size), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for data in progress.iterable:
        # write data read to the file
        f.write(data)
        # update the progress bar manually
        progress.update(len(data))