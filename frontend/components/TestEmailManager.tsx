"use client";

import React, { useState, useEffect } from "react";
import {
	Button,
	Modal,
	ModalBody,
	ModalContent,
	ModalFooter,
	ModalHeader,
	Input,
	Textarea,
	Dropdown,
	DropdownItem,
	DropdownMenu,
	DropdownTrigger,
	Table,
	TableHeader,
	TableBody,
	TableColumn,
	TableRow,
	TableCell,
	Chip,
	Switch,
	Divider,
	Card,
	CardBody,
	CardHeader
} from "@heroui/react";
import { addToast } from "@heroui/toast";
import { SearchIcon, PlusIcon, TrashIcon, EditIcon, PlayIcon, StopIcon } from "@/components/icons";

interface TestEmail {
	id: string;
	company_name: string;
	application_status: string;
	received_at: string;
	job_title: string;
	subject: string;
	email_from: string;
	email_body: string;
	is_demo_email: boolean;
	category?: string;
	notes?: string;
}

interface TestEmailManagerProps {
	apiUrl: string;
}

const APPLICATION_STATUSES = [
	"application confirmation",
	"rejection",
	"availability request",
	"information request",
	"assessment sent",
	"interview invitation",
	"did not apply - inbound request",
	"action required from company",
	"hiring freeze notification",
	"withdrew application",
	"offer made",
	"false positive"
];

export default function TestEmailManager({ apiUrl }: TestEmailManagerProps) {
	const [isOpen, setIsOpen] = useState(false);
	const [isAddModalOpen, setIsAddModalOpen] = useState(false);
	const [isEditModalOpen, setIsEditModalOpen] = useState(false);
	const [isDemoMode, setIsDemoMode] = useState(false);
	const [testEmails, setTestEmails] = useState<TestEmail[]>([]);
	const [searchTerm, setSearchTerm] = useState("");
	const [loading, setLoading] = useState(false);
	const [selectedEmail, setSelectedEmail] = useState<TestEmail | null>(null);
	const [categories, setCategories] = useState<string[]>([]);

	// Form state for adding/editing emails
	const [formData, setFormData] = useState({
		company_name: "",
		application_status: "",
		subject: "",
		job_title: "",
		email_from: "",
		email_body: "",
		category: "",
		notes: ""
	});

	useEffect(() => {
		fetchTestEmails();
		fetchCategories();
		checkDemoMode();
	}, []);

	const fetchTestEmails = async () => {
		try {
			const response = await fetch(`${apiUrl}/test-emails`, {
				method: "GET",
				credentials: "include"
			});
			if (response.ok) {
				const data = await response.json();
				setTestEmails(data);
			}
		} catch (error) {
			console.error("Error fetching test emails:", error);
		}
	};

	const fetchCategories = async () => {
		try {
			const response = await fetch(`${apiUrl}/test-email-categories`, {
				method: "GET",
				credentials: "include"
			});
			if (response.ok) {
				const data = await response.json();
				setCategories(data);
			}
		} catch (error) {
			console.error("Error fetching categories:", error);
		}
	};

	const checkDemoMode = async () => {
		// Check if demo mode is enabled by looking for demo emails
		const hasDemoEmails = testEmails.some(email => email.is_demo_email);
		setIsDemoMode(hasDemoEmails);
	};

	const enableDemoMode = async () => {
		setLoading(true);
		try {
			const response = await fetch(`${apiUrl}/enable-demo-mode`, {
				method: "POST",
				credentials: "include"
			});
			if (response.ok) {
				const data = await response.json();
				setIsDemoMode(true);
				await fetchTestEmails();
				addToast({
					title: "Demo Mode Enabled",
					description: `Loaded ${data.loaded_count} demo emails`,
					color: "success"
				});
			}
		} catch (error) {
			addToast({
				title: "Error",
				description: "Failed to enable demo mode",
				color: "danger"
			});
		} finally {
			setLoading(false);
		}
	};

	const disableDemoMode = async () => {
		setLoading(true);
		try {
			const response = await fetch(`${apiUrl}/disable-demo-mode`, {
				method: "POST",
				credentials: "include"
			});
			if (response.ok) {
				setIsDemoMode(false);
				await fetchTestEmails();
				addToast({
					title: "Demo Mode Disabled",
					description: "Demo mode has been disabled",
					color: "success"
				});
			}
		} catch (error) {
			addToast({
				title: "Error",
				description: "Failed to disable demo mode",
				color: "danger"
			});
		} finally {
			setLoading(false);
		}
	};

	const searchEmails = async () => {
		if (!searchTerm.trim()) {
			await fetchTestEmails();
			return;
		}

		try {
			const response = await fetch(`${apiUrl}/search-test-emails?q=${encodeURIComponent(searchTerm)}`, {
				method: "GET",
				credentials: "include"
			});
			if (response.ok) {
				const data = await response.json();
				setTestEmails(data);
			}
		} catch (error) {
			addToast({
				title: "Error",
				description: "Failed to search emails",
				color: "danger"
			});
		}
	};

	const addTestEmail = async () => {
		try {
			const response = await fetch(`${apiUrl}/add-test-email`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				credentials: "include",
				body: JSON.stringify(formData)
			});

			if (response.ok) {
				const data = await response.json();
				await fetchTestEmails();
				setIsAddModalOpen(false);
				resetForm();
				addToast({
					title: "Success",
					description: "Test email added successfully",
					color: "success"
				});
			} else {
				const error = await response.json();
				addToast({
					title: "Error",
					description: error.detail || "Failed to add test email",
					color: "danger"
				});
			}
		} catch (error) {
			addToast({
				title: "Error",
				description: "Failed to add test email",
				color: "danger"
			});
		}
	};

	const updateTestEmail = async () => {
		if (!selectedEmail) return;

		try {
			const response = await fetch(`${apiUrl}/update-test-email/${selectedEmail.id}`, {
				method: "PUT",
				headers: {
					"Content-Type": "application/json"
				},
				credentials: "include",
				body: JSON.stringify(formData)
			});

			if (response.ok) {
				await fetchTestEmails();
				setIsEditModalOpen(false);
				resetForm();
				addToast({
					title: "Success",
					description: "Test email updated successfully",
					color: "success"
				});
			} else {
				const error = await response.json();
				addToast({
					title: "Error",
					description: error.detail || "Failed to update test email",
					color: "danger"
				});
			}
		} catch (error) {
			addToast({
				title: "Error",
				description: "Failed to update test email",
				color: "danger"
			});
		}
	};

	const deleteTestEmail = async (emailId: string) => {
		try {
			const response = await fetch(`${apiUrl}/delete-test-email/${emailId}`, {
				method: "DELETE",
				credentials: "include"
			});

			if (response.ok) {
				await fetchTestEmails();
				addToast({
					title: "Success",
					description: "Test email deleted successfully",
					color: "success"
				});
			} else {
				addToast({
					title: "Error",
					description: "Failed to delete test email",
					color: "danger"
				});
			}
		} catch (error) {
			addToast({
				title: "Error",
				description: "Failed to delete test email",
				color: "danger"
			});
		}
	};

	const openEditModal = (email: TestEmail) => {
		setSelectedEmail(email);
		setFormData({
			company_name: email.company_name,
			application_status: email.application_status,
			subject: email.subject,
			job_title: email.job_title,
			email_from: email.email_from,
			email_body: email.email_body,
			category: email.category || "",
			notes: email.notes || ""
		});
		setIsEditModalOpen(true);
	};

	const resetForm = () => {
		setFormData({
			company_name: "",
			application_status: "",
			subject: "",
			job_title: "",
			email_from: "",
			email_body: "",
			category: "",
			notes: ""
		});
		setSelectedEmail(null);
	};

	const getStatusColor = (status: string) => {
		const normalized = status.toLowerCase();
		switch (normalized) {
			case "offer made":
				return "success";
			case "rejection":
				return "danger";
			case "interview invitation":
				return "primary";
			case "assessment sent":
				return "secondary";
			case "availability request":
				return "warning";
			case "application confirmation":
				return "default";
			default:
				return "default";
		}
	};

	const filteredEmails = testEmails.filter(email =>
		email.company_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
		email.subject.toLowerCase().includes(searchTerm.toLowerCase()) ||
		email.job_title.toLowerCase().includes(searchTerm.toLowerCase())
	);

	return (
		<>
			<Button
				color="primary"
				variant="bordered"
				onPress={() => setIsOpen(true)}
				startContent={<EditIcon size={16} />}
			>
				Manage Test Emails
			</Button>

			<Modal size="5xl" isOpen={isOpen} onOpenChange={setIsOpen}>
				<ModalContent>
					{(onClose) => (
						<>
							<ModalHeader>Test Email Manager</ModalHeader>
							<ModalBody>
								{/* Demo Mode Controls */}
								<Card className="mb-4">
									<CardHeader>
										<h3 className="text-lg font-semibold">Demo Mode</h3>
									</CardHeader>
									<CardBody>
										<div className="flex items-center justify-between">
											<div>
												<p className="text-sm text-gray-600">
													Demo mode uses test emails instead of real Gmail data for live presentations.
												</p>
											</div>
											<div className="flex items-center gap-4">
												<Switch
													isSelected={isDemoMode}
													onValueChange={isDemoMode ? disableDemoMode : enableDemoMode}
													isDisabled={loading}
												/>
												<Button
													color={isDemoMode ? "danger" : "success"}
													variant="bordered"
													size="sm"
													onPress={isDemoMode ? disableDemoMode : enableDemoMode}
													isLoading={loading}
													startContent={isDemoMode ? <StopIcon size={16} /> : <PlayIcon size={16} />}
												>
													{isDemoMode ? "Disable Demo" : "Enable Demo"}
												</Button>
											</div>
										</div>
									</CardBody>
								</Card>

								<Divider className="my-4" />

								{/* Search and Add Controls */}
								<div className="flex items-center justify-between mb-4">
									<div className="flex items-center gap-2 flex-1 max-w-md">
										<Input
											placeholder="Search emails..."
											value={searchTerm}
											onChange={(e) => setSearchTerm(e.target.value)}
											startContent={<SearchIcon size={16} />}
										/>
										<Button
											color="primary"
											variant="bordered"
											onPress={searchEmails}
										>
											Search
										</Button>
									</div>
									<Button
										color="success"
										onPress={() => setIsAddModalOpen(true)}
										startContent={<PlusIcon size={16} />}
									>
										Add Test Email
									</Button>
								</div>

								{/* Test Emails Table */}
								<div className="max-h-96 overflow-y-auto">
									<Table aria-label="Test emails table">
										<TableHeader>
											<TableColumn>Company</TableColumn>
											<TableColumn>Status</TableColumn>
											<TableColumn>Job Title</TableColumn>
											<TableColumn>Subject</TableColumn>
											<TableColumn>Type</TableColumn>
											<TableColumn>Actions</TableColumn>
										</TableHeader>
										<TableBody>
											{filteredEmails.map((email) => (
												<TableRow key={email.id}>
													<TableCell>{email.company_name}</TableCell>
													<TableCell>
														<Chip
															color={getStatusColor(email.application_status)}
															variant="flat"
															size="sm"
														>
															{email.application_status}
														</Chip>
													</TableCell>
													<TableCell>{email.job_title}</TableCell>
													<TableCell className="max-w-xs truncate">
														{email.subject}
													</TableCell>
													<TableCell>
														<Chip
															color={email.is_demo_email ? "primary" : "default"}
															variant="flat"
															size="sm"
														>
															{email.is_demo_email ? "Demo" : "Custom"}
														</Chip>
													</TableCell>
													<TableCell>
														<div className="flex items-center gap-2">
															<Button
																size="sm"
																variant="bordered"
																onPress={() => openEditModal(email)}
																isDisabled={email.is_demo_email}
															>
																<EditIcon size={14} />
															</Button>
															<Button
																size="sm"
																color="danger"
																variant="bordered"
																onPress={() => deleteTestEmail(email.id)}
															>
																<TrashIcon size={14} />
															</Button>
														</div>
													</TableCell>
												</TableRow>
											))}
										</TableBody>
									</Table>
								</div>
							</ModalBody>
							<ModalFooter>
								<Button color="danger" variant="light" onPress={onClose}>
									Close
								</Button>
							</ModalFooter>
						</>
					)}
				</ModalContent>
			</Modal>

			{/* Add Test Email Modal */}
			<Modal size="2xl" isOpen={isAddModalOpen} onOpenChange={setIsAddModalOpen}>
				<ModalContent>
					{(onClose) => (
						<>
							<ModalHeader>Add Test Email</ModalHeader>
							<ModalBody>
								<div className="space-y-4">
									<Input
										label="Company Name"
										value={formData.company_name}
										onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
										placeholder="Enter company name"
									/>
									<Dropdown>
										<DropdownTrigger>
											<Button variant="bordered" className="w-full justify-start">
												{formData.application_status || "Select Application Status"}
											</Button>
										</DropdownTrigger>
										<DropdownMenu
											aria-label="Application statuses"
											onSelectionChange={(keys) => {
												const status = Array.from(keys)[0] as string;
												setFormData({ ...formData, application_status: status });
											}}
										>
											{APPLICATION_STATUSES.map((status) => (
												<DropdownItem key={status}>{status}</DropdownItem>
											))}
										</DropdownMenu>
									</Dropdown>
									<Input
										label="Job Title"
										value={formData.job_title}
										onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
										placeholder="Enter job title"
									/>
									<Input
										label="Subject"
										value={formData.subject}
										onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
										placeholder="Enter email subject"
									/>
									<Input
										label="From Email"
										value={formData.email_from}
										onChange={(e) => setFormData({ ...formData, email_from: e.target.value })}
										placeholder="Enter sender email"
									/>
									<Dropdown>
										<DropdownTrigger>
											<Button variant="bordered" className="w-full justify-start">
												{formData.category || "Select Category (Optional)"}
											</Button>
										</DropdownTrigger>
										<DropdownMenu
											aria-label="Categories"
											onSelectionChange={(keys) => {
												const category = Array.from(keys)[0] as string;
												setFormData({ ...formData, category });
											}}
										>
											{categories.map((category) => (
												<DropdownItem key={category}>{category}</DropdownItem>
											))}
										</DropdownMenu>
									</Dropdown>
									<Textarea
										label="Email Body"
										value={formData.email_body}
										onChange={(e) => setFormData({ ...formData, email_body: e.target.value })}
										placeholder="Enter email body content"
										minRows={4}
									/>
									<Textarea
										label="Notes (Optional)"
										value={formData.notes}
										onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
										placeholder="Add any notes about this test email"
										minRows={2}
									/>
								</div>
							</ModalBody>
							<ModalFooter>
								<Button color="danger" variant="light" onPress={onClose}>
									Cancel
								</Button>
								<Button color="primary" onPress={addTestEmail}>
									Add Email
								</Button>
							</ModalFooter>
						</>
					)}
				</ModalContent>
			</Modal>

			{/* Edit Test Email Modal */}
			<Modal size="2xl" isOpen={isEditModalOpen} onOpenChange={setIsEditModalOpen}>
				<ModalContent>
					{(onClose) => (
						<>
							<ModalHeader>Edit Test Email</ModalHeader>
							<ModalBody>
								<div className="space-y-4">
									<Input
										label="Company Name"
										value={formData.company_name}
										onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
										placeholder="Enter company name"
									/>
									<Dropdown>
										<DropdownTrigger>
											<Button variant="bordered" className="w-full justify-start">
												{formData.application_status || "Select Application Status"}
											</Button>
										</DropdownTrigger>
										<DropdownMenu
											aria-label="Application statuses"
											onSelectionChange={(keys) => {
												const status = Array.from(keys)[0] as string;
												setFormData({ ...formData, application_status: status });
											}}
										>
											{APPLICATION_STATUSES.map((status) => (
												<DropdownItem key={status}>{status}</DropdownItem>
											))}
										</DropdownMenu>
									</Dropdown>
									<Input
										label="Job Title"
										value={formData.job_title}
										onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
										placeholder="Enter job title"
									/>
									<Input
										label="Subject"
										value={formData.subject}
										onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
										placeholder="Enter email subject"
									/>
									<Input
										label="From Email"
										value={formData.email_from}
										onChange={(e) => setFormData({ ...formData, email_from: e.target.value })}
										placeholder="Enter sender email"
									/>
									<Dropdown>
										<DropdownTrigger>
											<Button variant="bordered" className="w-full justify-start">
												{formData.category || "Select Category (Optional)"}
											</Button>
										</DropdownTrigger>
										<DropdownMenu
											aria-label="Categories"
											onSelectionChange={(keys) => {
												const category = Array.from(keys)[0] as string;
												setFormData({ ...formData, category });
											}}
										>
											{categories.map((category) => (
												<DropdownItem key={category}>{category}</DropdownItem>
											))}
										</DropdownMenu>
									</Dropdown>
									<Textarea
										label="Email Body"
										value={formData.email_body}
										onChange={(e) => setFormData({ ...formData, email_body: e.target.value })}
										placeholder="Enter email body content"
										minRows={4}
									/>
									<Textarea
										label="Notes (Optional)"
										value={formData.notes}
										onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
										placeholder="Add any notes about this test email"
										minRows={2}
									/>
								</div>
							</ModalBody>
							<ModalFooter>
								<Button color="danger" variant="light" onPress={onClose}>
									Cancel
								</Button>
								<Button color="primary" onPress={updateTestEmail}>
									Update Email
								</Button>
							</ModalFooter>
						</>
					)}
				</ModalContent>
			</Modal>
		</>
	);
} 