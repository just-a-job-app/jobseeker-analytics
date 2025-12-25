function processNewRows() {
  // ==========================================
  // 1. CONFIGURATION SECTION
  // ==========================================
  
  var spreadsheetId = "spreadsheets/d/{id}"; 
  var sheetName = "Form Responses 1"; 

  // *** IMPORTANT: UPDATE YOUR GOOGLE FORM CHECKBOXES TO MATCH THESE STRINGS EXACTLY ***
  var ALL_POSSIBLE_SIGNALS = {
    "Algorithms": [
      "Selected the Optimal Data Structure (e.g., Hash Map for O(1) lookups)",
      "Identified Time & Space Complexity (Correctly stated Big-O)",
      "Illustrated Optimal Solution (vs Brute force)",
      "Understood Trade-offs (e.g., Space vs. Time costs)"
    ],
    "Coding Standards": [
      "Code is DRY (Don't Repeat Yourself - used helper functions/abstractions)",
      "Variable Naming is Clear (e.g., 'multiplesOfThree' instead of 'x')",
      "Syntax is Clean (No major errors; compilable code)",
      "Proper Language Paradigms (Used language-specific features correctly)"
    ],
    "Communication": [
      "Paraphrased Question (Confirmed understanding before starting)",
      "Communicated Approach First (Did not jump straight into code)",
      "Talked While Coding (Explained logic as they typed)",
      "Clarified Assumptions (Asked about input range, null values, edge cases)"
    ],
    "Problem Solving": [
      "Systematic Approach (Logical flow, didn't guess)",
      "Handled Edge Cases (Null, Empty, Large Inputs, Negative numbers)",
      "Self-Corrected Bugs (Caught errors before running/submitting)",
      "Handled Follow-up Extensions (Adapted solution to new constraints)"
    ]
  };
  
  var headersConfig = {
    interviewDate: "Interview Date",
    interviewerTz: "Your Timezone (Interviewer)", 
    startTime: "Start Coding Time",
    endTime: "End Coding Time",
    email: "Candidate Email",
    name: "Candidate First Name",
    verdict: "Overall Recommendation",
    lcLink: "LeetCode Link",
    lcDiff: "LeetCode Difficulty",
    generalFeedback: "General Feedback / Additional Notes", // NEW
    
    // ALGORITHMS
    algoSignal: "Signals: Algorithms",
    algoScore: "Score: Algorithms (4 points)",
    algoComment: "Comments: Algorithms", // NEW

    // CODING
    codeSignal: "Signals: Coding",
    codeScore: "Score: Coding (4 points)",
    codeComment: "Comments: Coding", // NEW

    // COMMUNICATION
    commSignal: "Signals: Communication",
    commScore: "Score: Communication (4 points)",
    commComment: "Comments: Communication", // NEW

    // PROBLEM SOLVING
    probSignal: "Signals: Problem-Solving",
    probScore: "Score: Problem-Solving (4 points)",
    probComment: "Comments: Problem-Solving" // NEW
  };

  // ==========================================
  // 2. SETUP & VALIDATION
  // ==========================================

  try {
    var spreadsheet = SpreadsheetApp.openById(spreadsheetId);
  } catch(e) {
    console.error("Error: Could not open spreadsheet. Check your ID.");
    return;
  }

  var sheet = spreadsheet.getSheetByName(sheetName);
  if (!sheet) {
    console.error("Could not find tab: " + sheetName);
    return;
  }

  var lastRow = sheet.getLastRow();
  var lastCol = sheet.getLastColumn();
  if (lastRow < 2) return; 

  var data = sheet.getRange(1, 1, lastRow, lastCol).getValues();
  var headers = data[0];

  var statusColIndex = headers.indexOf("Email Status");
  if (statusColIndex === -1) {
    sheet.getRange(1, lastCol + 1).setValue("Email Status");
    statusColIndex = lastCol;
    data = sheet.getRange(1, 1, lastRow, lastCol + 1).getValues(); 
  }

  var colMap = {};
  for (var key in headersConfig) {
    var index = headers.indexOf(headersConfig[key]);
    if (index === -1) {
      console.error("Missing Column: " + headersConfig[key]);
      return; 
    }
    colMap[key] = index;
  }

  // ==========================================
  // 3. ROW PROCESSING LOOP
  // ==========================================
  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var emailStatus = row[statusColIndex];

    if (emailStatus === "" || emailStatus === undefined) {
      var recipientEmail = row[colMap.email];
      
      if (recipientEmail) {
        
        var interviewCount = 0;
        for (var j = 1; j <= i; j++) {
          if (data[j][colMap.email] === recipientEmail) {
            interviewCount++;
          }
        }

        sendEmailForRow(row, colMap, interviewCount, ALL_POSSIBLE_SIGNALS);
        
        sheet.getRange(i + 1, statusColIndex + 1).setValue("Sent"); 
        console.log("Sent email for row " + (i + 1));
      } else {
        sheet.getRange(i + 1, statusColIndex + 1).setValue("Skipped - No Email");
      }
      Utilities.sleep(500); 
    }
  }
}

// ==========================================
// 4. EMAIL GENERATION FUNCTION
// ==========================================
function sendEmailForRow(row, map, count, allSignalsConfig) {
  var name = row[map.name] || "Candidate";
  var lcLink = row[map.lcLink] || "#";
  var lcDiff = row[map.lcDiff] || "N/A";
  var generalNote = row[map.generalFeedback] || "";
  
  // --- VERDICT CALCULATION ---
  var s1 = parseInt(row[map.algoScore]) || 0;
  var s2 = parseInt(row[map.codeScore]) || 0;
  var s3 = parseInt(row[map.commScore]) || 0;
  var s4 = parseInt(row[map.probScore]) || 0;

  var average = (s1 + s2 + s3 + s4) / 4;
  var verdict = "";

  if (average === 4.0) verdict = "Strong Hire";
  else if (average >= 3.0) verdict = "Hire";
  else if (average >= 2.0) verdict = "No Hire";
  else verdict = "Strong No Hire";

  verdict += " (Average Score: " + average.toFixed(2) + "/4)";

  // --- LOGISTICS ---
  var rawDate = row[map.interviewDate];
  var rawTz = row[map.interviewerTz] || ""; 
  var rawStart = row[map.startTime];
  var rawEnd = row[map.endTime];
  var timeZone = Session.getScriptTimeZone();

  var formattedDate = (rawDate instanceof Date) ? Utilities.formatDate(rawDate, timeZone, "MMMM d, yyyy") : "N/A";
  var formattedStart = (rawStart instanceof Date) ? Utilities.formatDate(rawStart, timeZone, "h:mm a") : "";
  var formattedEnd = (rawEnd instanceof Date) ? Utilities.formatDate(rawEnd, timeZone, "h:mm a") : "";

  var durationStr = "N/A";
  if (rawStart instanceof Date && rawEnd instanceof Date) {
    var diffMs = rawEnd.getTime() - rawStart.getTime();
    var diffMins = Math.floor(diffMs / 60000); 
    durationStr = diffMins + " mins";
  }

  var timeOfDay = "Session";
  if (rawStart instanceof Date) {
    var hour = parseInt(Utilities.formatDate(rawStart, timeZone, "H")); 
    if (hour < 12) timeOfDay = "Morning Session";
    else if (hour < 17) timeOfDay = "Afternoon Session";
    else timeOfDay = "Evening Session";
  }

  // --- HTML HEADER ---
  var htmlBody = "<div style='font-family: Helvetica, Arial, sans-serif; color: #333; max-width: 600px; line-height: 1.5;'>" +
                 "<h2 style='color: #202124; margin-bottom: 5px;'>Interview Feedback</h2>" +
                 "<p>Hi " + name + ",</p>" +
                 "<p>Here is the feedback from your coding session:</p>" +
                 
                 "<div style='background-color: #f1f3f4; padding: 15px; border-radius: 5px; margin: 15px 0; font-size: 14px; color: #444;'>" +
                    "<div style='margin-bottom: 5px;'><strong>Date:</strong> " + formattedDate + "</div>" +
                    "<div style='margin-bottom: 5px;'><strong>" + timeOfDay + ":</strong> " + formattedStart + " - " + formattedEnd + " (" + rawTz + ")</div>" +
                    "<div><strong>Duration:</strong> " + durationStr + "</div>" +
                 "</div>" +

                 "<div style='background-color: #e8f0fe; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 5px solid #1967d2;'>" +
                 "<h4 style='margin-top: 0; margin-bottom: 10px; color: #1967d2;'>Challenge Details</h4>" +
                 "<p style='margin: 5px 0;'><strong>Problem:</strong> <a href='" + lcLink + "'>" + lcLink + "</a></p>" +
                 "<p style='margin: 5px 0;'><strong>Difficulty:</strong> " + lcDiff + "</p>" +
                 "</div>" +
                 
                 "<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>";

  // --- DIMENSIONS LOOP ---
  var dimensions = [
    { name: "Algorithms", score: row[map.algoScore], selectedRaw: row[map.algoSignal], comment: row[map.algoComment] },
    { name: "Coding Standards", score: row[map.codeScore], selectedRaw: row[map.codeSignal], comment: row[map.codeComment] },
    { name: "Communication", score: row[map.commScore], selectedRaw: row[map.commSignal], comment: row[map.commComment] },
    { name: "Problem Solving", score: row[map.probScore], selectedRaw: row[map.probSignal], comment: row[map.probComment] }
  ];

  var lowestScore = 10;
  var lowestDimensions = [];

  dimensions.forEach(function(dim) {
    var scoreStr = dim.score ? dim.score.toString() : "N/A";
    var signalsHtml = "";
    
    // 1. Get List of Selected Signals
    var selectedList = smartSplitSignals(dim.selectedRaw ? dim.selectedRaw.toString() : "");
    var possibleList = allSignalsConfig[dim.name] || [];

    // 2. Build HTML List
    if (possibleList.length > 0) {
      signalsHtml = "<ul style='list-style-type: none; padding-left: 0; margin-top: 10px; margin-bottom: 0;'>";
      possibleList.forEach(function(signalText) {
        var isSelected = selectedList.some(function(s) { return s.trim() === signalText.trim(); });
        if (isSelected) {
          signalsHtml += "<li style='margin-bottom: 8px; color: #333; line-height: 1.4;'>" + 
                         "<span style='font-size: 1.1em; margin-right: 8px;'>&#9989;</span>" + 
                         signalText + 
                         "</li>";
        } else {
          signalsHtml += "<li style='margin-bottom: 8px; color: #aaa; line-height: 1.4;'>" + 
                         "<span style='font-size: 1.1em; margin-right: 8px; opacity: 0.5;'>&#10060;</span>" + 
                         signalText + 
                         "</li>";
        }
      });
      signalsHtml += "</ul>";
    } else {
       signalsHtml = "<p style='font-style: italic; color: #888; padding-left: 10px;'>Signal list not configured.</p>";
    }

    // 3. Add Comments Section (NEW)
    var commentHtml = "";
    if (dim.comment && dim.comment.toString().trim() !== "") {
      commentHtml = "<div style='margin-top: 15px; padding: 10px; background-color: #f1f1f1; border-left: 4px solid #aaa; font-style: italic; color: #555;'>" + 
                    "<strong>Comments:</strong> " + dim.comment + 
                    "</div>";
    }

    htmlBody += "<div style='background-color: #f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>" +
                "<table width='100%' cellpadding='0' cellspacing='0' border='0'><tr>" +
                "<td valign='top' style='padding-right: 15px;'><h3 style='margin: 0; color: #202124; font-size: 16px;'>" + dim.name + "</h3></td>" +
                "<td valign='top' align='right' width='160' style='min-width: 140px;'><span style='font-weight: bold; font-size: 14px; background-color: #fff; padding: 4px 8px; border-radius: 4px; border: 1px solid #ddd; display: inline-block;'>Score: " + scoreStr + "</span></td>" +
                "</tr></table>" +
                signalsHtml +
                commentHtml + // Inject Comment Here
                "</div>";

    // Lowest Score Logic
    var numericScore = parseInt(scoreStr); 
    if (!isNaN(numericScore)) {
      if (numericScore < lowestScore) {
        lowestScore = numericScore;
        lowestDimensions = [dim.name]; 
      } else if (numericScore === lowestScore) {
        lowestDimensions.push(dim.name); 
      }
    }
  });

  // --- RECOMMENDATION SECTION ---
  var recommendationHtml = "";
  if (lowestDimensions.length > 0) {
    var randomLowDim = lowestDimensions[Math.floor(Math.random() * lowestDimensions.length)];
    var advice = "";
    if (randomLowDim === "Algorithms") advice = "Aim to effortlessly illustrate several solutions along with their drawbacks. Select the most optimal algorithm to solve the problem and clearly display to your interviewer that you have a deep understanding of algorithms.";
    else if (randomLowDim === "Coding Standards") advice = "Aim to write working and clean code with no syntax errors. This helps display an outstanding understanding of paradigms in your chosen programming language.";
    else if (randomLowDim === "Communication") advice = "Throughout the interview, aim to communicate with perfect clarity. Ensure interviewer has no difficulty understanding your thought process, the trade-offs of the different approaches you are considering. Aim for well-organized and succinct answers.";
    else if (randomLowDim === "Problem Solving") advice = "Aim for a well-thought-out and accurate solution to the problem. Leave enough time to discuss trade-offs, related problems, alternatives while asking the interviewer clarifying questions.";

    recommendationHtml = "<div style='border: 1px dashed #fbbc04; background-color: #fff8e1; padding: 15px; border-radius: 8px; margin: 20px 0;'>" +
                         "<h4 style='margin: 0 0 5px 0; color: #b06000;'>&#128161; Top Recommendation for Next Time</h4>" +
                         "<p style='margin: 0; color: #555;'><strong>Area: " + randomLowDim + ".</strong> " + advice + "</p>" +
                         "</div>";
  }

  htmlBody += recommendationHtml;

  // --- GENERAL FEEDBACK SECTION (NEW) ---
  if (generalNote && generalNote.trim() !== "") {
    htmlBody += "<div style='margin: 20px 0; padding: 15px; background-color: #e6f4ea; border-radius: 8px; border-left: 5px solid #0f9d58;'>" +
                "<h3 style='margin-top: 0; color: #0f9d58; font-size: 16px;'>Additional Notes</h3>" +
                "<p style='margin: 0; color: #333;'>" + generalNote + "</p>" +
                "</div>";
  }

  // --- VERDICT & FOOTER ---
  var verdictColor = (verdict.toString().toLowerCase().includes("no")) ? "#d93025" : "#0f9d58";
  
  htmlBody += "<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>" +
              "<h3 style='margin-bottom: 5px;'>Overall Recommendation: <span style='color: " + verdictColor + ";'>" + verdict + "</span></h3>" +
              "<p style='color: #666; font-weight: bold;'>Total Sessions Completed: " + count + "</p>" +
              "<p style='color: #444; margin-top: 15px; font-style: italic;'>No matter the outcome, every interview is a success because you were here. You showed up, you practiced, and you're getting better every time.</p>" +
              "<p style='margin-top: 20px;'>Rooting for your success,<br>The Interview Team</p>" +
              "<hr style='border: 0; border-top: 1px solid #eee; margin: 30px 0;'>" +
              "<p style='font-size: 12px; color: #777; text-align: center;'>" +
                "Interviewing someone else? You can submit feedback in this format by filling out the form:<br>" +
                "<a href='https://forms.gle/8iVJW4aJPjLXajSK9' style='color: #1967d2; text-decoration: none;'>https://forms.gle/8iVJW4aJPjLXajSK9</a>" +
              "</p>" +
              "</div>";

  GmailApp.sendEmail(row[map.email], "Your Coding Interview Feedback", "", {htmlBody: htmlBody});
}

// ==========================================
// 5. HELPER: SMART SPLIT
// ==========================================
function smartSplitSignals(rawString) {
  if (!rawString) return [];
  var parts = rawString.split(', ');
  var result = [];
  var buffer = "";
  var insideParens = false;
  parts.forEach(function(part) {
    if (insideParens) {
      buffer += ", " + part; 
      if (part.includes(')')) { insideParens = false; result.push(buffer); buffer = ""; }
    } else {
      if (part.includes('(') && !part.includes(')')) { insideParens = true; buffer = part; } 
      else { result.push(part); }
    }
  });
  if (buffer) { result.push(buffer); }
  return result;
}
