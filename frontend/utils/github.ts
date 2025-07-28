import { Octokit } from "@octokit/rest";
import { createAppAuth } from "@octokit/auth-app";

interface CreateIssueParams {
	title: string;
	body: string;
	labels?: string[];
}

interface GitHubIssueResponse {
	success: boolean;
	issueNumber?: number;
	error?: string;
}

/**
 * Initialize GitHub App Octokit client
 */
function initializeGitHubClient(): Octokit | null {
	if (!process.env.GH_APP_ID || !process.env.GH_PRIVATE_KEY || !process.env.GH_INSTALLATION_ID) {
		return null;
	}

	try {
		return new Octokit({
			authStrategy: createAppAuth,
			auth: {
				appId: process.env.GH_APP_ID,
				privateKey: process.env.GH_PRIVATE_KEY,
				installationId: process.env.GH_INSTALLATION_ID
			}
		});
	} catch (error) {
		console.warn("Failed to initialize GitHub App authentication:", error);
		return null;
	}
}

/**
 * Create a GitHub issue
 */
export async function createGitHubIssue(params: CreateIssueParams): Promise<GitHubIssueResponse> {
	const { title, body, labels = ["📣 user feedback"] } = params;

	const appOctokit = initializeGitHubClient();
	if (!appOctokit) {
		return { success: false, error: "GitHub App not configured" };
	}

	try {
		const response = await appOctokit.issues.create({
			owner: "just-a-job-app",
			repo: "jobseeker-analytics",
			title,
			body,
			labels
		});

		return { success: true, issueNumber: response.data.number };
	} catch (error) {
		return { success: false, error: "Failed to create issue" };
	}
}
