import { cookies } from "next/headers";

import { Navbar } from "@/components/navbar";

export default async function NavbarSSR() {
	const apiUrl = process.env.NEXT_SERVER_API_URL!;
	const cookieStore = await cookies();
	const cookieHeader = cookieStore
		.getAll()
		.map((c) => `${c.name}=${c.value}`)
		.join("; ");
	let showLogin = false;

	try {
		const url = `${apiUrl}/me`;
		const res = await fetch(url, {
			headers: { cookie: cookieHeader },
			credentials: "include",
			cache: "no-store"
		});
		showLogin = res.ok;
	} catch (e) {
		console.log("[NavbarSSR] fetch failed", { apiUrl, error: String(e), url: `${apiUrl}/me` });
		showLogin = false;
	}

	return <Navbar showLogin={showLogin} />;
}
