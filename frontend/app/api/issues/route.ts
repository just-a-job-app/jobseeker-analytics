import { NextResponse } from "next/server";
import { Octokit } from "@octokit/rest";
import { createAppAuth } from "@octokit/auth-app";

// Initialize the GitHub App authentication
const appOctokit = new Octokit({
	authStrategy: createAppAuth,
	auth: {
		appId: process.env.GITHUB_APP_ID,
		privateKey: process.env.GITHUB_PRIVATE_KEY,
		installationId: process.env.GITHUB_INSTALLATION_ID
	}
});

export async function POST(request: Request) {
	try {
		const { title, description } = await request.json();

		if (!title || !description) {
			return NextResponse.json({ error: "Title and description are required" }, { status: 400 });
		}

		const response = await appOctokit.issues.create({
			owner: "just-a-job-app",
			repo: "jobseeker-analytics",
			title: `[BUG]: ${title}`,
			body: description,
			labels: ["📣 user feedback"]
		});

		return NextResponse.json({ success: true, issueNumber: response.data.number }, { status: 201 });
	} catch (error) {
		console.error("Error creating issue:", error);
		return NextResponse.json({ error: "Failed to submit issue" }, { status: 500 });
	}
}
