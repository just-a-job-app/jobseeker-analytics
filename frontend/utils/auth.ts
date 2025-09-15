export async function checkAuth(apiUrl: string): Promise<boolean> {
	try {
		const response = await fetch(`${apiUrl}/me`, {
			method: "GET",
			credentials: "include"
		});

		if (response.ok) {
			markReturningUser();
			return true;
		}

		if (response.status === 401) {
			clearReturningUser();
			return false;
		}

		return false;
	} catch {
		return false;
	}
}

export function markReturningUser(): void {
	if (typeof window === "undefined") return;
	try {
		localStorage.setItem("hasLoggedInBefore", "1");
	} catch {
		return;
	}
}

export function clearReturningUser(): void {
	if (typeof window === "undefined") return;
	try {
		localStorage.removeItem("hasLoggedInBefore");
	} catch {
		return;
	}
}

export function hasLoggedInBefore(): boolean {
	if (typeof window === "undefined") return false;
	try {
		return localStorage.getItem("hasLoggedInBefore") === "1";
	} catch {
		return false;
	}
}
