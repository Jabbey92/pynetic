import re
from os import environ

import requests
from github import Github, GithubException
from mdutils import MdUtils

print(f">>> Starting Code Stats Process for {(REPO_NAME := environ.get('GITHUB_REPOSITORY', ''))}")

# Setup Constants
OUT_PATH = ".github/stats/Code Statistics.md"
LOC_API_URL = f"https://api.codetabs.com/v1/loc?github={REPO_NAME}"
KEYS = ["📝Files", "〰️Lines", "🗨️Blanks", "🙈Comments", "👨‍💻Lines of Code"]

# Setup globals
repository = Github(environ.get("INPUT_GITHUB_TOKEN")).get_repo(REPO_NAME)
languages_table = ["", *KEYS]
language_chart_table = {}
lines_chart_table = []

# Create Markdown File
md_file = MdUtils("Lines Of Code.md")
md_file.create_md_file()
md_file.new_header(1, f"📊 Code Statistics for {REPO_NAME.split('/')[-1]}")

# Populate Languages Table
for num_languages, language in enumerate(map(dict.values, requests.get(LOC_API_URL).json()), 1):
    lang, *language_values = (lang, *_, lines) = language
    languages_table.extend(language)

    if lang == "Total":
        lines_chart_table.extend(language_values)
        break

    language_chart_table[lang] = lines

else:
    num_languages = 0

# Add Languages Pie Chart
md_file.new_line("```mermaid")
md_file.new_line("pie title Language Distribution")
for language, lines in language_chart_table.items():
    md_file.new_line(f'    "{language}" : {lines}')
md_file.new_line("```")
md_file.new_line()

# Add Lines Pie Chart
md_file.new_line('<div class="right">')
md_file.new_line()
md_file.new_line("```mermaid")
md_file.new_line("pie title Code Distribution")
for line_type, lines in zip(KEYS, lines_chart_table):
    md_file.new_line(f'    "{line_type}" : {lines}')
md_file.new_line("```")
md_file.new_line()
md_file.new_line("</div>")
md_file.new_line()

# Languages Table
md_file.new_header(2, "👨‍💻Languages")
md_file.new_line()
md_file.new_table(columns=6, rows=num_languages + 1, text=languages_table)

# Updated contents for markdown file
# For some reason mdutils insists on putting 2 lines
# after every new line. I'm just taking those lines
# out so mermaid formats correctly
new_content = re.sub(r"\s{2}$(?<!\d)", "", md_file.get_md_text(), flags=re.M)[1:]

# Update Readme
try:
    repository.update_file(
        OUT_PATH,
        "📈 Update stats file",
        new_content,
        (
            content[0]
            if isinstance(
                content := repository.get_contents(OUT_PATH),
                list,
            )
            else content
        ).sha,
    )

except GithubException as err:
    repository.create_file(OUT_PATH, "🎉 Create stats file", new_content)

print(f">>> Code Stats Process for {REPO_NAME} Finished")
