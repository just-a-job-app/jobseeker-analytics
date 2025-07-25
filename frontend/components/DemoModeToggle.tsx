"use client";

import React, { useState, useEffect } from "react";
import { Button, Switch, Tooltip } from "@heroui/react";
import { addToast } from "@heroui/toast";
import { PlayIcon, StopIcon } from "@/components/icons";

interface DemoModeToggleProps {
	apiUrl: string;
}

export default function DemoModeToggle({ apiUrl }: DemoModeToggleProps) {
	const [isDemoMode, setIsDemoMode] = useState(false);
	const [loading, setLoading] = useState(false);

	useEffect(() => {
		// Check if demo mode is enabled by looking for demo emails
		checkDemoMode();
	}, []);

	const checkDemoMode = async () => {
		try {
			// Try to get demo mode status from session
			const response = await fetch(`${apiUrl}/test-emails`, {
				method: "GET",
				credentials: "include"
			});
			if (response.ok) {
				const data = await response.json();
				// Check if there are demo emails or if demo mode is enabled in session
				const hasDemoEmails = data.some((email: any) => email.is_demo_email);
				setIsDemoMode(hasDemoEmails);
			}
		} catch (error) {
			// If not authenticated, just show as disabled (default state)
			console.log("Demo mode check failed (likely not authenticated):", error);
			setIsDemoMode(false);
		}
	};

	const toggleDemoMode = async () => {
		setLoading(true);
		try {
			const endpoint = isDemoMode ? "disable-demo-mode" : "enable-demo-mode";
			const response = await fetch(`${apiUrl}/${endpoint}`, {
				method: "POST",
				credentials: "include"
			});

			if (response.ok) {
				const data = await response.json();
				setIsDemoMode(!isDemoMode);
				
				if (!isDemoMode) {
					addToast({
						title: "Dev Mode Enabled",
						description: `Using mock Gmail API with ${data.loaded_count || 0} test emails`,
						color: "success"
					});
				} else {
					addToast({
						title: "Dev Mode Disabled",
						description: "Using real Gmail API",
						color: "success"
					});
				}

				// Refresh the page to show updated data
				window.location.reload();
			} else if (response.status === 401 || response.status === 403) {
				// Not authenticated - show info toast
				addToast({
					title: "Authentication Required",
					description: "Please log in to toggle developer mode",
					color: "warning"
				});
			}
		} catch (error) {
			addToast({
				title: "Error",
				description: `Failed to ${isDemoMode ? 'disable' : 'enable'} dev mode`,
				color: "danger"
			});
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="flex items-center gap-2">
			<Tooltip content="Toggle between real Gmail API and mock data for development">
				<Switch
					isSelected={isDemoMode}
					onValueChange={toggleDemoMode}
					isDisabled={loading}
					size="sm"
				/>
			</Tooltip>
			<Tooltip content="Toggle between real Gmail API and mock data for development">
				<Button
					color={isDemoMode ? "danger" : "success"}
					variant="bordered"
					size="sm"
					onPress={toggleDemoMode}
					isLoading={loading}
					startContent={isDemoMode ? <StopIcon size={14} /> : <PlayIcon size={14} />}
				>
					{isDemoMode ? "Dev Mode" : "Dev Mode"}
				</Button>
			</Tooltip>
		</div>
	);
} 