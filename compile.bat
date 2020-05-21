@echo off

echo -- 1/2 -- Updating quaver...

:: We only case about the current state and not the entire git history of Quaver, so
:: --depth 1 is used to reduce the total size of the downloaded files
if not exist .\Quaver\ git clone https://github.com/Quaver/Quaver --depth 1
cd Quaver
git pull > null
git submodule update --init Quaver.API > null
cd ..

echo -- 2/2 -- Generating files...

pandoc .\base_template.md --metadata-file=".\metadata.yaml" -o .\quaver_plugin_guide.md -t gfm --filter=.\filters\insertStrippedCode.py --quiet
pandoc .\base_template.md --metadata-file=".\metadata.yaml" -o .\quaver_plugin_guide.pdf --pdf-engine-opt="-quiet" -F panflute --quiet

echo -- Done!
