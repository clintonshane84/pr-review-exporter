# pr-review-exporter
`pr-review-exporter` is a Python-based tool designed to extract review histories, conversations, comments, and associated code changes from GitHub repositories. By leveraging the GitHub API, this project enables developers, researchers, and data scientists to collect valuable data for training AI models focused on understanding and generating human-like responses in the context of software development discussions, code reviews, and issue resolutions.

With `pr-review-exporter`, users can authenticate with their GitHub account and specify one or more repositories to extract data from. The tool fetches the desired information, including review histories, conversations, comments, and the corresponding code diffs or resolutions that address those conversations.

The extracted data is then structured and converted into a JSONL (JSON Lines) format, making it suitable for direct ingestion and processing by AI models or other data analysis pipelines. This standardized format ensures compatibility and ease of integration with various machine learning frameworks and tools.

Key features of `pr-review-exporter` include:

- **Authentication**: Securely authenticate with GitHub using personal access tokens or other supported methods.
- **Repository Selection**: Select one or multiple GitHub repositories to extract data from.
- **Data Extraction**: Fetch review histories, conversations, comments, and associated code changes or resolutions.
- **JSONL Conversion**: Convert the extracted data into a structured JSONL format for easy processing and analysis.
- **Customizable Filtering**: Apply filters to extract specific types of data or narrow down the scope based on user-defined criteria.
- **Incremental Updates**: Support for incremental data updates, allowing users to fetch new data while preserving previously collected information.

Whether you're a researcher studying code review practices, a developer interested in analyzing project conversations, or a data scientist training AI models for code generation or issue resolution, `pr-review-exporter` provides a powerful and efficient solution for acquiring the necessary data from GitHub repositories.

Get started with `pr-review-exporter` today and unlock valuable insights into software development processes, code reviews, and conversations within your projects.
