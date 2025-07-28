import { NextResponse, NextRequest } from "next/server";

interface SubscriberData {
	email: string;
	name?: string;
	formType?: "waitlist" | "setup";
}

async function createSubscriber(data: SubscriberData, apiKey: string): Promise<Response> {
	return fetch("https://api.convertkit.com/v4/subscribers", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-Kit-Api-Key": apiKey
		},
		body: JSON.stringify({
			email_address: data.email,
			first_name: data.name,
			state: "inactive"
		})
	});
}

async function addSubscriberToForm(email: string, apiKey: string, formId: string): Promise<Response> {
	const url = `https://api.convertkit.com/v4/forms/${formId}/subscribers`;
	return fetch(url, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-Kit-Api-Key": apiKey
		},
		body: JSON.stringify({ email_address: email })
	});
}

export async function POST(req: NextRequest) {
	try {
		const { email, name, formType = "waitlist" } = await req.json();

		if (!email || !email.includes("@")) {
			return NextResponse.json({ success: false, message: "Valid email is required" }, { status: 400 });
		}

		const apiKey = process.env.CONVERTKIT_API_KEY;

		// Choose the appropriate form ID based on the formType parameter
		const formId = formType === "setup" ? process.env.CONVERTKIT_SETUP_FORM_ID : process.env.CONVERTKIT_FORM_ID;

		if (!apiKey || !formId) {
			return NextResponse.json({ success: false, message: "Server configuration error" }, { status: 500 });
		}

		// Step 1: Create an inactive subscriber
		const createResponse = await createSubscriber({ email, name, formType }, apiKey);

		if (!createResponse.ok) {
			const error = await createResponse.json();
			return NextResponse.json({ success: false, message: "Failed to add to list" }, { status: 500 });
		}

		// Step 2: Add subscriber to form
		const formResponse = await addSubscriberToForm(email, apiKey, formId);

		if (!formResponse.ok) {
			return NextResponse.json(
				{ success: false, message: "Added to list but confirmation may fail" },
				{ status: 500 }
			);
		}

		const successMessage =
			formType === "setup" ? "Setup session requested successfully" : "Successfully added to waitlist";

		return NextResponse.json({
			success: true,
			message: successMessage
		});
	} catch (error) {
		return NextResponse.json({ success: false, message: "Server error" }, { status: 500 });
	}
}
