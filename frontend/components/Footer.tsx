"use client";

import { useRouter } from "next/navigation";
import { Button } from "@heroui/react";

import { ExternalLinkIcon, GoogleIcon } from "@/components/icons";
import { useFireworks } from "@/hooks/useFireworks";

const Footer = () => {
	const router = useRouter();
	const apiUrl = process.env.NEXT_PUBLIC_API_URL!;
	const { triggerFireworks } = useFireworks();

	const handleGoogleLogin = () => {
		router.push(`${apiUrl}/login`);
	};

	return (
		<footer className="border-t py-12 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
			<div className="container mx-auto px-4">
				<div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center md:text-left">
					<div>
						<h3 className="text-lg font-semibold mb-4 text-emerald-700">Just A Job App</h3>
						<p className="text-default-500 mb-4">
							Designed for ambitious professionals. <br />
							Built to fix a broken system.
						</p>
					</div>

					<div>
						<h3 className="text-lg font-semibold mb-4 text-emerald-700">
							Get the Unfair Advantage in Your Job Search.
						</h3>
						<p className="text-default-500 mb-4">
							Join 300+ ambitious professionals on the priority list. We'll give you early access to the
							tools that turn your hidden achievements into your next big opportunity.
						</p>
						<a
							className="flex items-center justify-center md:justify-start gap-2 text-sm text-amber-600 hover:text-amber-700 transition-colors font-medium"
							href="#waitlist"
							onClick={() => triggerFireworks("waitlist")}
						>
							<ExternalLinkIcon size={16} />
							Request Early Access
						</a>
					</div>
					<div>
						<h3 className="text-lg font-semibold mb-4 text-emerald-700">Already a Beta Tester?</h3>
						<p className="text-default-500 mb-4">Log In Below.</p>
						<Button
							className="bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
							startContent={<GoogleIcon size={16} />}
							variant="bordered"
							onPress={handleGoogleLogin}
						>
							Login with Google
						</Button>
					</div>
				</div>

				<div className="mt-12 pt-6 border-t text-center text-sm text-default-500">
					<p className="mt-2 text-amber-600 font-medium">© {new Date().getFullYear()} Just A Job App</p>
				</div>
			</div>
		</footer>
	);
};

export default Footer;
