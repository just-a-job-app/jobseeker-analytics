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
		const { message } = await request.json();

		if (!message) {
			return NextResponse.json({ error: "Message is required" }, { status: 400 });
		}

		const response = await appOctokit.issues.create({
			owner: "just-a-job-app",
			repo: "jobseeker-analytics",
			title: `Feedback: ${message.slice(0, 50)}...`,
			body: `User Feedback:\n\n${message}`,
			labels: ["📣 user feedback"]
		});

		return NextResponse.json({ success: true, issueNumber: response.data.number }, { status: 201 });
	} catch (error) {
		console.error("Error creating feedback issue:", error);
		return NextResponse.json({ error: "Failed to submit feedback" }, { status: 500 });
	}
}
