import { EmailIcon, ExternalLinkIcon } from "@/components/icons";

const Footer = () => {
	return (
		<footer className="border-t py-12 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
			<div className="container mx-auto px-4">
				<div className="grid grid-cols-1 md:grid-cols-3 gap-8">
					<div>
						<h3 className="text-lg font-semibold mb-4">Support open source</h3>
						<p className="text-default-500 mb-4">
							If you're a developer, please consider starring us on GitHub to help spread the word about
							this project.
						</p>
						<a
							className="flex items-center gap-2 text-sm text-default-500 hover:text-foreground transition-colors"
							href="https://github.com/just-a-job-app/jobseeker-analytics"
							rel="noopener noreferrer"
							target="_blank"
						>
							<ExternalLinkIcon size={16} />
							Star us on GitHub
						</a>
					</div>

					<div>
						<h3 className="text-lg font-semibold mb-4">Bookmark these free resources</h3>
						<ul className="space-y-2 text-default-500">
							<li>
								<a
									className="flex items-center gap-2 text-sm hover:text-foreground transition-colors"
									href="https://hiring.cafe/"
									rel="noopener noreferrer"
									target="_blank"
								>
									<ExternalLinkIcon size={16} />
									Hiring Cafe - The best job board out there
								</a>
							</li>
							<li>
								<a
									className="flex items-center gap-2 text-sm hover:text-foreground transition-colors"
									href="https://www.phyl.org/join-jsc"
									rel="noopener noreferrer"
									target="_blank"
								>
									<ExternalLinkIcon size={16} />
									Never Search Alone - Find your Job Search Crew
								</a>
							</li>
							<li>
								<a
									className="flex items-center gap-2 text-sm hover:text-foreground transition-colors"
									href="https://randsinrepose.com/welcome-to-rands-leadership-slack/"
									rel="noopener noreferrer"
									target="_blank"
								>
									<ExternalLinkIcon size={16} />
									Rands Community - The one Slack you get to keep
								</a>
							</li>
						</ul>
					</div>

					<div>
						<h3 className="text-lg font-semibold mb-4">Contact us</h3>
						<div className="space-y-4">
							<a
								className="flex items-center gap-2 text-sm text-default-500 hover:text-foreground transition-colors"
								href="https://discord.gg/5tTT6WVQyw"
								rel="noopener noreferrer"
								target="_blank"
							>
								<ExternalLinkIcon size={16} />
								Join our Discord
							</a>
							<a
								className="flex items-center gap-2 text-sm text-default-500 hover:text-foreground transition-colors"
								href="mailto:help@justajobapp.com"
							>
								<EmailIcon size={16} />
								help@justajobapp.com
							</a>
							<a
								className="flex items-center gap-2 text-sm text-default-500 hover:text-foreground transition-colors"
								href="mailto:security@justajobapp.com"
							>
								<EmailIcon size={16} />
								security@justajobapp.com
							</a>
						</div>
					</div>
				</div>

				<div className="mt-12 pt-6 border-t text-center text-sm text-default-500">
					<p className="mt-2">© {new Date().getFullYear()} Just a Job App (JAJA)</p>
				</div>
			</div>
		</footer>
	);
};

export default Footer;
