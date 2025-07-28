import { NextResponse } from "next/server";

import { createGitHubIssue } from "../../../utils/github";

export async function POST(request: Request) {
	try {
		const { message } = await request.json();

		if (!message) {
			return NextResponse.json({ error: "Message is required" }, { status: 400 });
		}

		const result = await createGitHubIssue({
			title: `Feedback: ${message.slice(0, 50)}...`,
			body: `User Feedback:\n\n${message}`
		});

		if (!result.success) {
			return NextResponse.json({ error: result.error || "Failed to submit feedback" }, { status: 500 });
		}

		return NextResponse.json({ success: true, issueNumber: result.issueNumber }, { status: 201 });
	} catch (error) {
		return NextResponse.json({ error: "Failed to submit feedback" }, { status: 500 });
	}
}
