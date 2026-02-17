AI Experts Assignment (Python)

In this project, I demonstrated my ability to:

Set up a small Python project that runs reliably both locally and in Docker

Pin dependencies for reproducible installs

Write focused tests that reproduce a bug

Implement a minimal, reviewable fix

What I Did
1) Dockerfile

I created a Dockerfile so the project can run the test suite in a non-interactive, CI-style environment.

Installed dependencies from requirements.txt

Included and pinned pytest in requirements.txt

Configured the container to run tests by default using:

CMD ["python", "-m", "pytest", "-v"]

2) requirements.txt

I created a requirements.txt file with pinned package versions to ensure reproducible installs, for example:

package==x.y.z

3) Running Tests

Locally:

I installed dependencies and ran the test suite:

pip install -r requirements.txt
python -m pytest -v


With Docker:

I built the Docker image and ran tests inside the container:

docker build -t ai-experts-assignment .
docker run --rm ai-experts-assignment

4) Finding and Fixing a Bug

I identified a bug in the code by analyzing the logic and running tests

I wrote tests that reproduced the bug (these failed on the original code)

I applied the smallest possible fix to make the tests pass

I ensured the change was minimal and reviewable, without refactoring unrelated code

5) EXPLANATION.md

I created an EXPLANATION.md (max 250 words) explaining:

What the bug was

Why it happened

Why my fix resolves it

One edge case my tests do not cover

Submission

I submitted this solution as a public GitHub repository using the Google Form link provided.

