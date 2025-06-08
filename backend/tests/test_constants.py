from pathlib import Path

SUBJECT_LINE = "Invitation from an unknown sender: Interview with TestCompanyName @ Thu May 2, 2024 11:00am - 12pm (PDT) (appuser@gmail.com)"
SAMPLE_MESSAGE = {
    "id": "abc123",
    "threadId": "abc123",
    "labelIds": ["IMPORTANT", "CATEGORY_PERSONAL", "Label_1"],
    "snippet": "Interview with TestCompanyName Unknown sender This event from recruitername@testcompanyname.com won&#39;t appear in your calendar unless you say you know the sender. Know this sender? When Thursday May 9, 2024 ⋅ 02:40pm –",
    "payload": {
        "partId": "",
        "mimeType": "multipart/mixed",
        "filename": "",
        "headers": [
            {"name": "Delivered-To", "value": "appuser@gmail.com"},
            {
                "name": "Received",
                "value": "by 2024:abc:6000:2000:b0:200:1000:5000 with SMTP id cub;        Thu, 2 May 2024 16:45:00 -0700 (PDT)",
            },
            {
                "name": "X-Received",
                "value": "by 2024:abc:6000:2000:b0:200:1000:5000 with SMTP id def567-890jkl.9.000000000000;        Thu, 2 May 2024 16:45:00 -0700 (PDT)",
            },
            {
                "name": "ARC-Seal",
                "value": "redacted-ARC-value",
            },
            {
                "name": "ARC-Message-Signature",
                "value": "i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-00000000;        h=to:from:subject:date:message-id:sender:reply-to:mime-version         :dkim-signature:dkim-signature;        bh=pqr123;        fh=AZ123/PST=;        b=GAH",
            },
            {
                "name": "ARC-Authentication-Results",
                "value": "i=1; mx.google.com;       dkim=pass header.i=@google.com header.s=10101101 header.b=WOOHOO;       dkim=pass header.i=@testcompanyname.com header.s=google header.b=di8r;       spf=pass (google.com: domain of recruitername@testcompanyname.com designates 000.00.000.00 as permitted sender) smtp.mailfrom=recruitername@testcompanyname.com;       dmarc=pass (p=NONE sp=NONE dis=NONE) header.from=testcompanyname.com",
            },
            {"name": "Return-Path", "value": "<recruitername@testcompanyname.com>"},
            {
                "name": "Received",
                "value": "from mail-fff-a00.google.com (mail-fff-a00.google.com. [000.00.000.00])        by mx.google.com with SMTPS id def567-890mno.0.2024.05.02.16.45.00        for <appuser@gmail.com>        (Google Transport Security);        Thu, 2 May 2024 16:45:00 -0700 (PDT)",
            },
            {
                "name": "Received-SPF",
                "value": "pass (google.com: domain of recruitername@testcompanyname.com designates 000.00.000.00 as permitted sender) client-ip=000.00.000.00;",
            },
            {
                "name": "Authentication-Results",
                "value": "mx.google.com;       dkim=pass header.i=@google.com header.s=10101101 header.b=WOOHOO;       dkim=pass header.i=@testcompanyname.com header.s=google header.b=di8r;       spf=pass (google.com: domain of recruitername@testcompanyname.com designates 000.00.000.00 as permitted sender) smtp.mailfrom=recruitername@testcompanyname.com;       dmarc=pass (p=NONE sp=NONE dis=NONE) header.from=testcompanyname.com",
            },
            {
                "name": "DKIM-Signature",
                "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=google.com; s=10101101; t=1111111111; x=1111111111; dara=google.com;        h=to:from:subject:date:message-id:sender:reply-to:mime-version:from         :to:cc:subject:date:message-id:reply-to;        bh=pqr123;        b=GAH",
            },
            {
                "name": "DKIM-Signature",
                "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=testcompanyname.com; s=google; t=1111111111; x=1111111111; dara=google.com;        h=to:from:subject:date:message-id:sender:reply-to:mime-version:from         :to:cc:subject:date:message-id:reply-to;        bh=pqr123;        b=GAH",
            },
            {
                "name": "X-Google-DKIM-Signature",
                "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=1e100.net; s=10101101; t=1111111111; x=1111111111;        h=to:from:subject:date:message-id:sender:reply-to:mime-version         :x-gm-message-state:from:to:cc:subject:date:message-id:reply-to;        bh=pqr123;        b=BLAH",
            },
            {
                "name": "X-Gm-Message-State",
                "value": "AGH",
            },
            {
                "name": "X-Google-Smtp-Source",
                "value": "AGH",
            },
            {"name": "MIME-Version", "value": "1.0"},
            {
                "name": "X-Received",
                "value": "by 2222:abc:600:2000:d0:777:9000:4000 with SMTP id def567-890ghi.10.1111111111566; Thu, 2 May 2024 16:45:00 -0700 (PDT)",
            },
            {
                "name": "Reply-To",
                "value": "Recruiter Name <recruitername@testcompanyname.com>",
            },
            {
                "name": "Sender",
                "value": "Google Calendar <calendar-notification@google.com>",
            },
            {
                "name": "Message-ID",
                "value": "<calendar-98a@google.com>",
            },
            {"name": "Date", "value": "Thu, 2 May 2024 16:45:00 +0000"},
            {
                "name": "Subject",
                "value": "Invitation from an unknown sender: Interview with TestCompanyName @ Thu May 2, 2024 11:00am - 12pm (PDT) (appuser@gmail.com)",
            },
            {
                "name": "From",
                "value": "Recruiter Name <recruitername@testcompanyname.com>",
            },
            {"name": "To", "value": "appuser@gmail.com"},
            {
                "name": "Content-Type",
                "value": 'multipart/mixed; boundary="000000000000"',
            },
        ],
        "body": {"size": 0},
        "parts": [
            {
                "partId": "0",
                "mimeType": "multipart/alternative",
                "filename": "",
                "headers": [
                    {
                        "name": "Content-Type",
                        "value": 'multipart/alternative; boundary="000000000000"',
                    }
                ],
                "body": {"size": 0},
                "parts": [
                    {
                        "partId": "0.0",
                        "mimeType": "text/plain",
                        "filename": "",
                        "headers": [
                            {
                                "name": "Content-Type",
                                "value": 'text/plain; charset="UTF-8"; format=flowed; delsp=yes',
                            },
                            {"name": "Content-Transfer-Encoding", "value": "base64"},
                        ],
                        "body": {
                            "size": 2000,
                            "data": "abc",
                        },
                    },
                    {
                        "partId": "0.1",
                        "mimeType": "text/html",
                        "filename": "",
                        "headers": [
                            {
                                "name": "Content-Type",
                                "value": 'text/html; charset="UTF-8"',
                            },
                            {
                                "name": "Content-Transfer-Encoding",
                                "value": "quoted-printable",
                            },
                        ],
                        "body": {
                            "size": 30000,
                            "data": "abc",
                        },
                    },
                    {
                        "partId": "0.2",
                        "mimeType": "text/calendar",
                        "filename": "invite.ics",
                        "headers": [
                            {
                                "name": "Content-Type",
                                "value": 'text/calendar; charset="UTF-8"; method=REQUEST',
                            },
                            {"name": "Content-Transfer-Encoding", "value": "7bit"},
                        ],
                        "body": {
                            "attachmentId": "",
                            "size": 1000,
                        },
                    },
                ],
            },
            {
                "partId": "1",
                "mimeType": "application/ics",
                "filename": "invite.ics",
                "headers": [
                    {
                        "name": "Content-Type",
                        "value": 'application/ics; name="invite.ics"',
                    },
                    {
                        "name": "Content-Disposition",
                        "value": 'attachment; filename="invite.ics"',
                    },
                    {"name": "Content-Transfer-Encoding", "value": "base64"},
                ],
                "body": {
                    "attachmentId": "",
                    "size": 1000,
                },
            },
        ],
    },
    "sizeEstimate": 33333,
    "historyId": "22222222",
    "internalDate": "1111111111000",
}

DESIRED_PASS_APPLIED_EMAIL_FILTER_SUBJECT = [
    "Thank you for your Application!",
    "Jobba, your application was sent to The Huts",
    "Your Interview with",
    "Thank you for your job application"
]

DESIRED_FAIL_APPLIED_EMAIL_FILTER_FROM = [
    "do-not-reply@wateringapp.net",  # made up, would be better to capture the real example
    "no-reply@comet.zillow.com",
    "IRCC.DoNotReply-NePasRepondre.IRCC@prson-srpel.apps.cic.gc.ca",
    "jobs-noreply@linkedin.com",
    "insights@careerseeker.accenture.com",
    "personalemail@domain.com",
    "accenture@myworkday.com",
    "hello@stratascratch.com"
]

DESIRED_FAIL_APPLIED_EMAIL_FILTER_SUBJECT = [
    "Apply to",
    "Apply now",
    "New job",
    "Job Search Council Matching - Next Steps"
]

DESIRED_PASS_APPLIED_EMAIL_FILTER_FROM = ["hit-reply@linkedin.com", "myworkday.com"]

SAMPLE_FILTER_PATH = Path(__file__).parent / "sample_base_filter.yaml"
EXPECTED_SAMPLE_QUERY_STRING = """(subject:"application has been submitted" 
    OR (subject:"application to" AND subject:"successfully submitted") 
    OR from:"do-not-reply@jobs.microsoft.com" 
    AND -from:"no-reply@comet.zillow.com" 
    AND -subject:"watering")"""
