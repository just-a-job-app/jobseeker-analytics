import { NextResponse } from "next/server";

import { createGitHubIssue } from "../../../utils/github";

export async function POST(request: Request) {
	try {
		const { title, description } = await request.json();

		if (!title || !description) {
			return NextResponse.json({ error: "Title and description are required" }, { status: 400 });
		}

		const result = await createGitHubIssue({
			title: `[BUG]: ${title}`,
			body: description
		});

		if (!result.success) {
			return NextResponse.json({ error: result.error || "Failed to submit issue" }, { status: 500 });
		}

		return NextResponse.json({ success: true, issueNumber: result.issueNumber }, { status: 201 });
	} catch (error) {
		return NextResponse.json({ error: "Failed to submit issue" }, { status: 500 });
	}
}
