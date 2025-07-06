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
		},
		{
			label: "TestPage",
			href: "/testpage"
		}
	],
	navMenuItems: [
		{
			label: "Profile",
			href: "/profile"
		},
		{
			label: "Dashboard",
			href: "/dashboard"
		},
		{
			label: "Projects",
			href: "/projects"
		},
		{
			label: "Team",
			href: "/team"
		},
		{
			label: "Calendar",
			href: "/calendar"
		},
		{
			label: "Settings",
			href: "/settings"
		},
		{
			label: "Help & Feedback",
			href: "/help-feedback"
		},
		{
			label: "Logout",
			href: "/logout"
		}
	],
	links: {
		github: "https://github.com/lnovitz/jobseeker-analytics",
		sponsor: "https://github.com/sponsors/lnovitz"
	}
};
