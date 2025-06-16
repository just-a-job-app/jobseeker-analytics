import { NextResponse } from "next/server";

const MAILERLITE_API_KEY = process.env.MAILERLITE_API_KEY;
const MAILERLITE_FOUNDING_GROUP_ID = process.env.MAILERLITE_FOUNDING_GROUP_ID;
const MAILERLITE_UPDATES_GROUP_ID = process.env.MAILERLITE_UPDATES_GROUP_ID;

export async function POST(request: Request) {
	try {
		const { email, type } = await request.json();

		if (!email) {
			return NextResponse.json(
				{ error: "Email is required" },
				{ status: 400 }
			);
		}

		if (!type || !["founding", "updates"].includes(type)) {
			return NextResponse.json(
				{ error: "Invalid subscription type" },
				{ status: 400 }
			);
		}

		if (!MAILERLITE_API_KEY || !MAILERLITE_FOUNDING_GROUP_ID || !MAILERLITE_UPDATES_GROUP_ID) {
			console.error("Missing MailerLite configuration");
			return NextResponse.json(
				{ error: "Server configuration error" },
				{ status: 500 }
			);
		}

		const groupId = type === "founding" ? MAILERLITE_FOUNDING_GROUP_ID : MAILERLITE_UPDATES_GROUP_ID;

		const response = await fetch("https://api.mailerlite.com/api/v2/subscribers", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-MailerLite-ApiKey": MAILERLITE_API_KEY,
			},
			body: JSON.stringify({
				email,
				resubscribe: true,
				autoresponders: true,
				type: "active",
				groups: [groupId],
			}),
		});

		if (!response.ok) {
			const error = await response.json();
			console.error("MailerLite API error:", error);
			return NextResponse.json(
				{ error: "Failed to subscribe" },
				{ status: response.status }
			);
		}

		return NextResponse.json({ success: true });
	} catch (error) {
		console.error("Subscription error:", error);
		return NextResponse.json(
			{ error: "Internal server error" },
			{ status: 500 }
		);
	}
}
