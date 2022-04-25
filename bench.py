import os
import platform
from shutil import which

# Constants

repos = [
    {"name": "TypeScript", "source_path": "src"},
    {"name": "eslint", "source_path": "."},
    {"name": "freeCodeCamp", "source_path": "."},
    {"name": "tldraw", "source_path": "."},
    {"name": "tools", "source_path": "."},
    {"name": "vue", "source_path": "."},
    {"name": "webpack", "source_path": "."},
]

DPRINT_JSON = """
{
  "incremental": true,
  "typescript": {},
  "includes": ["**/*.{ts,tsx,js,jsx,cjs,mjs}"],
  "excludes": ["**/node_modules"],
  "plugins": ["https://plugins.dprint.dev/typescript-0.65.1.wasm"]
}
"""

# Check if the proper tools are installed


def is_installed(tool):
    return which(tool) is not None


if not is_installed("hyperfine"):
    raise "hyperfine is not installed. Please install at https://github.com/sharkdp/hyperfine"

if not is_installed("rome"):
    raise "rome is not installed. Please install at https://github.com/rome/tools"

if not is_installed("dprint"):
    raise "dprint is not installed. Please install at https://github.com/dprint/dprint"


dir_path = os.path.dirname(os.path.realpath(__file__))
output_file = open(
    "{dir}/bench-{platform}.md".format(dir=dir_path, platform=platform.platform()), "w"
)

for repo in repos:
    try:
        dprint_file = open(
            "{dir}/{repo}/{source}/dprint.json".format(
                dir=dir_path, repo=repo["name"], source=repo["source_path"]
            ),
            "w",
        )
    except:
        raise "Could not find repository. Did you initialize with `git submodule init` and `git submodule update`?"
    
    dprint_file.write(DPRINT_JSON)
    dprint_file.close()

    os.system(
        'cd {repo}/{source} && hyperfine --warmup 5 --runs 20 -i --prepare "git reset --hard" \
--export-markdown {dir}/bench_{repo}.md "dprint fmt" "rome format --write --skip-errors ."'.format(
            repo=repo["name"], source=repo["source_path"], dir=dir_path
        )
    )

    markdown_file_path = "{dir}/bench_{repo}.md".format(repo=repo["name"], dir=dir_path)
    markdown_file = open(markdown_file_path, "r")
    output_file.write("\n# {repo}\n".format(repo=repo["name"]))
    output_file.write(markdown_file.read())
    os.remove(markdown_file_path)

output_file.close()
os.system("git submodule foreach git reset --hard")
os.system("git submodule foreach git clean -f")
