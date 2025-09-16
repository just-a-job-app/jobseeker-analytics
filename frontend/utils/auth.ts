export async function checkAuth(apiUrl: string): Promise<boolean> {
	try {
		const response = await fetch(`${apiUrl}/me`, {
			method: "GET",
			credentials: "include"
		});

		if (response.ok) {
			return true;
		}

		if (response.status === 401) {
			return false;
		}

		return false;
	} catch {
		return false;
	}
}
