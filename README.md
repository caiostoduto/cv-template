> Simpler Curriculum Vitae agentic AI automation with git versioning

Suggestion: Put all your experience at `rendercv/cv.yaml` and let agentic take things out and put things in

## Requirements

- [just](https://github.com/casey/just#installation)
- [uv](https://github.com/astral-sh/uv#installation)

## How to use

### Manually

```sh
# 1. Install all dependencies and prepare the project
$ just install

# 2. Make changes to `rendercv/cv.yaml`
# ...

# 3. Generate and render the rendercv file
$ just generate # or 'just watch'

# 4. Check the generated PDF (repeat step 2 as many times as you need!)
# ...

# 5. Add the changes to your private repo (optionally)
$ just git-add `branch_name` # I recommend giving it a name like "company-job_title-YYYY-MM-DD"
$ git commit -m "..."
$ git push
```

### Agentic

```sh
# 1. Install all dependencies and prepare the project
$ just install

# 2. Ask an agentic AI (e.g.: AntiGravity IDE, GitHub Copilot, etc.) to
#     make changes (use PROMPT.md as guide).
#
#    If you use PROMPT.md as a guide,
#     it'll probably already have done the manually section steps 2 to 5,
#     otherwise just follow steps 3 to 5, it is non-destructive!
# ...
```

## Results

### Preview

[![Preview](output/John_Doe_CV_1.png)](output/John_Doe_CV.pdf)
[![Preview](output/John_Doe_CV_2.png)](output/John_Doe_CV.pdf)
[![Preview](output/John_Doe_CV_3.png)](output/John_Doe_CV.pdf)

### Considerations

