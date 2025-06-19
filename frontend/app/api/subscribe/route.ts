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

		// First, create or update the subscriber
		const subscriberResponse = await fetch("https://connect.mailerlite.com/api/subscribers", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"Accept": "application/json",
				"Authorization": `Bearer ${MAILERLITE_API_KEY}`,
			},
			body: JSON.stringify({
				"email": email,
				"groups": [groupId],
			}),
		});

		if (!subscriberResponse.ok) {
			const error = await subscriberResponse.json();
			console.error("MailerLite API error:", error);
			return NextResponse.json(
				{ error: "Failed to create subscriber" },
				{ status: subscriberResponse.status }
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
