"use client";

import { useEffect } from "react";
import { Card } from "@heroui/react";

export default function LogoutPage() {
	const apiUrl = process.env.NEXT_PUBLIC_API_URL!;

	useEffect(() => {
		// Show the UI for a brief moment, then navigate for server-side logout
		const timer = setTimeout(() => {
			window.location.href = `${apiUrl}/logout`;
		}, 600);
		return () => clearTimeout(timer);
	}, [apiUrl]);

	return (
		<div className="min-h-[70vh] flex items-center justify-center px-4">
			<Card className="max-w-md w-full p-8 text-center bg-gradient-to-br from-amber-50 to-emerald-50 dark:from-amber-950/30 dark:to-emerald-950/30 border border-amber-200 dark:border-amber-800/50">
				<div className="flex flex-col items-center gap-4">
					<img alt="Logo" src="/logo.png" className="h-12 w-12" />
					<h1 className="text-2xl font-semibold bg-clip-text text-transparent bg-gradient-to-r from-amber-600 to-emerald-600">
						Logging you out
					</h1>
					<p className="text-default-600 dark:text-default-400">Please wait a moment…</p>
					<div className="mt-2 h-8 w-8 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
				</div>
			</Card>
		</div>
	);
}
