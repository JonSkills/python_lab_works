import re
from datetime import datetime
from pathlib import Path

folder = Path(__file__).parent
text = (folder / "mailbox.txt").read_text(encoding="utf-8", errors="replace")
lines = text.splitlines()

def find_all(pattern, data=text, flags=0):
    return re.findall(pattern, data, flags)

def add_section(result, title, values):
    values = list(values)
    result.append(f"{title} (count: {len(values)})")
    result.extend(str(value) for value in values)
    result.append("")

# 1. Sender account names
sender_emails = find_all(r"(?m)^From:\s*([^\s<>]+)")
sender_accounts = [email.split("@", 1)[0] for email in sender_emails]

# 2. Revision numbers from Details
revisions = find_all(r"(?m)^Details:.*?[?&]rev=(\d+)", flags=re.IGNORECASE)

# 3. Count emails by mbox separator lines
email_count = len(find_all(r"(?m)^From\s+\S+@\S+"))

# 4. Sender domains
sender_domains = [email.split("@", 1)[1] for email in sender_emails if "@" in email]

# 5. Confidence scores
confidence_scores = find_all(r"(?m)^X-DSPAM-Confidence:\s*([0-9.]+)")

# 6. Log messages, from Log: to the dashed separator
log_messages = []
for i, line in enumerate(lines):
    if line.strip() == "Log:":
        log_lines = []
        for next_line in lines[i + 1:]:
            if re.fullmatch(r"-{6,}", next_line.strip()):
                break
            log_lines.append(next_line)
        log_messages.append("\n".join(log_lines).strip())

# 7. Sent dates, formatted as Mon D, YYYY
sent_dates = []
for value in find_all(r"(?m)^Date:\s*(.+)$"):
    try:
        parsed = datetime.strptime(value.strip(), "%a, %d %b %Y %H:%M:%S %z")
        sent_dates.append(parsed.strftime("%b %d, %Y").replace(" 0", " "))
    except ValueError:
        sent_dates.append(value.strip())

# 8. ESMTP IDs
esmtp_ids = find_all(r"\bwith ESMTP id\s+([A-Za-z0-9]+)", flags=re.IGNORECASE)

# 9. IP addresses found in Received header lines and their continuations
received_blocks = re.findall(r"(?m)^Received:.*(?:\n[ \t]+.*)*", text)
ip_addresses = []
for block in received_blocks:
    ip_addresses.extend(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", block))

# 10. Subjects containing "gradebook"
gradebook_subjects = [
    subject for subject in find_all(r"(?m)^Subject:\s*(.+)$")
    if "gradebook" in subject.lower()
]

# 11. Cyrus versions
cyrus_versions = find_all(r"\bCyrus\s+(v[\d.]+)", flags=re.IGNORECASE)

# 12. SMTP IDs
smtp_ids = find_all(r"\bwith SMTP ID\s+([A-Za-z0-9]+)", flags=re.IGNORECASE)

# 13. Message-ID without angle brackets and domain
message_ids = [
    value.split("@", 1)[0]
    for value in find_all(r"(?m)^Message-ID:\s*<([^>]+)>")
]

# 14. Number of lines
line_count = len(lines)

# 15. Lines containing "java"
java_lines = [line for line in lines if "java" in line.lower()]

# 16. Time values
time_values = find_all(r"\b(\d{2}:\d{2}:\d{2})\b")

# 17–18. Longest and shortest non-empty lines
nonempty_lines = [line for line in lines if line.strip()]
longest_line = max(nonempty_lines, key=len) if nonempty_lines else ""
shortest_line = min(nonempty_lines, key=len) if nonempty_lines else ""

result = []
add_section(result, "1. Sender account names", sender_accounts)
add_section(result, "2. Revision numbers (Details)", revisions)
result.append(f"3. Number of emails: {email_count}\n")
add_section(result, "4. Sender domains", sender_domains)
add_section(result, "5. X-DSPAM-Confidence scores", confidence_scores)
add_section(result, "6. Log messages", log_messages)
add_section(result, "7. Sent dates", sent_dates)
add_section(result, "8. ESMTP IDs", esmtp_ids)
add_section(result, "9. IP addresses in Received headers", ip_addresses)
add_section(result, "10. Subjects containing 'gradebook'", gradebook_subjects)
add_section(result, "11. Cyrus versions", cyrus_versions)
add_section(result, "12. SMTP IDs", smtp_ids)
add_section(result, "13. Message-ID values (without domain)", message_ids)
result.append(f"14. Number of lines: {line_count}\n")
add_section(result, "15. Lines containing 'java'", java_lines)
add_section(result, "16. Time values (HH:MM:SS)", time_values)
result.extend([
    "17. Longest non-empty line:",
    longest_line,
    f"Length: {len(longest_line)} characters\n",
    "18. Shortest non-empty line:",
    shortest_line,
    f"Length: {len(shortest_line)} characters\n",
])

(folder / "output.txt").write_text("\n".join(result), encoding="utf-8")
print("Готово! Результаты сохранены в output.txt")
print(f"Количество писем: {email_count}")
print(f"Количество строк: {line_count}")
