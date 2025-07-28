export type SiteConfig = typeof siteConfig;

export const siteConfig = {
	name: "Just A Job App",
	description: "Built by jobseekers, for jobseekers.",
	navItems: [
		{
			label: "Home",
			href: "/"
		},
		{
			label: "Dashboard",
			href: "/dashboard"
		}
	],
	navMenuItems: [
		{
			label: "Preview Dashboard",
			href: "/preview/dashboard"
		},
		{
			label: "Preview Processing",
			href: "/preview/processing"
		},
		{
			label: "Dashboard",
			href: "/dashboard"
		},
		{
			label: "Logout",
			href: "/logout"
		},
		{
			label: "Login",
			href: "/login"
		}
	],
	links: {
		github: "https://github.com/just-a-job-app/jobseeker-analytics",
		sponsor: "https://github.com/sponsors/lnovitz"
	}
};
