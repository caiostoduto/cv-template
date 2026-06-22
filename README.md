> Simpler Curriculum Vitae agentic AI automation with git versioning

Suggestion: Put all your experience at `rendercv/cv.yaml` and let agentic take things out and put things in

## Requirements

- [just](https://github.com/casey/just#installation)
- [uv](https://github.com/astral-sh/uv#installation)

## How to use

1. [Create a fork of this repository](https://github.com/caiostoduto/cv-template/fork) and [change its visibility to private](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility#changing-a-repositorys-visibility)
2. Clone the forked repository

### Manually

```sh
# 3. Install all dependencies and prepare the project
$ just install

# 4. Make changes to `rendercv/cv.yaml`
# ...

# 5. Generate and render the rendercv file
$ just generate # or 'just watch'

# 6. Check the generated PDF (repeat step 2 as many times as you need!)
# ...

# 7. Add the changes to your private repo (optionally)
$ just git-add `branch_name` # I recommend giving it a name like "company-job_title-YYYY-MM-DD"
$ git commit -m "..."
$ git push
```

### Agentic

```sh
# 3. Install all dependencies and prepare the project
$ just install

# 4. Ask an agentic AI (e.g.: AntiGravity IDE, GitHub Copilot, etc.) to
#     make changes (use PROMPT.md as guide).
#
#    If you use PROMPT.md as a guide,
#     it'll probably already have done the steps 4 to 7 from the previous section 'Manually',
#     otherwise just follow steps 5 to 7, it is non-destructive!
# ...
```

## Results

### Preview

[![Preview](output/John_Doe_CV_1.png)](output/John_Doe_CV.pdf)
[![Preview](output/John_Doe_CV_2.png)](output/John_Doe_CV.pdf)
[![Preview](output/John_Doe_CV_3.png)](output/John_Doe_CV.pdf)

### Considerations

