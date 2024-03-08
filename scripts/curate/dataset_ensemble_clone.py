# SPDX-FileCopyrightText: (c) 2024 EvalPlus Team
#
# SPDX-License-Identifier: Apache-2.0

"""
! Note: not fully usable. You might encounter:
github.GithubException.GithubException: 422 {"message": "Validation Failed", "errors": [{"message": "The listed users and repositories cannot be searched either because the resources do not exist o
r you do not have permission to view them.", "resource": "Search", "field": "q", "code": "invalid"}], "documentation_url": "https://docs.github.com/v3/search/"}
"""

import json
from datetime import datetime
from typing import TypedDict

import git
import tempdir
from fire import Fire
from tqdm.auto import tqdm

lang2suffix = {
    "python": [".py"],
    "go": [".go"],
    "c++": [".cpp", ".hpp", ".cc", ".hh", ".cxx", ".hxx", ".c", ".h"],
    "java": [".java"],
    "typescript": [".ts"],
    "php": [".php"],
    "rust": [".rs"],
}


def main(
    target_path: str = f"repoqa-{datetime.now().isoformat()}.json",
):

    # read /scripts/cherrypick/lists.json
    with open("scripts/cherrypick/lists.json") as f:
        lists = json.load(f)

    for lang, repos in lists.items():
        lang_suffix = lang2suffix[lang]
        for repo in tqdm(repos):
            repo_name = repo["repo"]
            commit_sha = repo["commit_sha"]
            entrypoint = repo["entrypoint_path"]

            print(f"Visiting https://github.com/{repo_name}/tree/{commit_sha}")

            if repo.get("content"):
                print(f"Skipping {repo_name} as it already has content.")
                continue

            with tempdir.TempDir() as temp_dir:
                gh_repo = git.Repo.clone_from(
                    f"https://github.com/{repo_name}.git",
                    temp_dir,
                )
                gh_repo.git.checkout(commit_sha)

                files_to_include = []
                for entry in gh_repo.commit().tree.traverse():
                    if entry.path.startswith(entrypoint) and any(
                        [entry.path.endswith(suffix) for suffix in lang_suffix]
                    ):
                        files_to_include.append(entry.abspath)

                repo["content"] = {}
                for path in files_to_include:
                    with open(path, "r") as f:
                        repo["content"][path] = f.read()

    with open(target_path, "w") as f_out:
        json.dump(lists, f_out)


if __name__ == "__main__":
    Fire(main)
