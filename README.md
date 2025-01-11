# Ansible Playbook: Panorama/Paloalto Content update

## **Synopsis**

This Ansible role automates the process of checking, downloading, and installing content updates on Palo Alto Networks firewalls. It also includes error handling and email notification capabilities to ensure the process is transparent and traceable. The role is designed to be used in environments where regular content updates are required for Palo Alto firewalls.

---

## **Variables**

The following variables are used in this role:

| **Variable**               | **Type** | **Default** | **Comments**                                                                 |
|----------------------------|----------|-------------|------------------------------------------------------------------------------|
| **`username`**             | String   | -           | **Mandatory**. Username for the Palo Alto firewall. Retrieved from `ANSIBLE_NET_USERNAME` environment variable. |
| **`password`**             | String   | -           | **Mandatory**. Password for the Palo Alto firewall. Retrieved from `ANSIBLE_NET_PASSWORD` environment variable. |
| **`jump_host`**            | String   | -           | **Mandatory**. The host to which tasks are delegated (e.g., a jump host).    |
| **`server`**               | String   | -           | **Mandatory**. IP address of the Palo Alto firewall.                        |
| **`tower_user_email`**     | String   | -           | **Mandatory**. Email address to which the report will be sent.              |
| **`tower_job_id`**         | String   | -           | **Mandatory**. Job ID for the email subject.                                |
| **`smtp_server`**          | String   | -           | **Mandatory**. SMTP server for sending emails.                              |
| **`smtp_port`**            | Integer  | -           | **Mandatory**. SMTP port for sending emails.                                |
| **`sender_email`**         | String   | -           | **Mandatory**. Sender email address for the email notification.             |
| **`recipient_email`**      | List     | -           | **Mandatory**. List of recipient email addresses.                           |
| **`subject`**              | String   | -           | **Mandatory**. Subject of the email notification.                           |
| **`body`**                 | String   | -           | **Mandatory**. Body of the email notification.                              |
| **`subtype`**              | String   | `plain`     | **Optional**. Email body subtype (`html` or `plain`). Default is `plain`.   |
| **`attachment_path`**      | String   | -           | **Optional**. Path to the attachment file for the email.                    |

---

## **Results from Execution**

The role can finish with the following return codes:

| **Return Code Group** | **Return Code** | **Comments**                                                                 |
|-----------------------|-----------------|------------------------------------------------------------------------------|
| **Success**           | 0               | The content update process completed successfully.                           |
| **Error**             | 10              | Failed to check content upgrade status. Check firewall IP and credentials.  |
| **Error**             | 11              | Failed to download content upgrade. Check firewall IP and credentials.      |
| **Error**             | 12              | Failed to check content upgrade status after download.                      |
| **Error**             | 13              | Failed to install the latest content upgrade.                               |

---

## **Procedure**

### **1. Check Content Upgrade Status**
- The playbook sends an XML command to the firewall to check the current content update status.
- If the check fails, it sets a fact with an error message and continues execution.

### **2. Download Content Upgrade**
- If updates are available, the playbook downloads the latest content upgrade.
- The download status and job ID are captured for further verification.

### **3. Check Content Upgrade Status After Download**
- After downloading the update, the playbook verifies the content update status again.
- It checks if the downloaded version matches the target version.

### **4. Install Latest Content Upgrade**
- If the downloaded version is not already installed, the playbook installs it.
- The installation status and job ID are captured for further verification.

### **5. Send Email Notification**
- After completing the content update process, the playbook sends an email report.
- The email includes details such as the latest version, release date, download status, and current status.

---

## **Support**

For issues or questions, please contact the development team:
- **Support Contact**: Mahendra Pratap Sengar
- **Support Email**: mahendras.tulipit@gmail.com

---

## **Deployment**

### **Ansible Tower Configuration**
1. **Project Setup**:
   - Create a new project and point this repo.
   - Create a job template with credentials
   - Create a repo to call the role as below:

     ```yml
     ---
      - name: Panorama content update playbook
        hosts: localhost # keep localhost only
        gather_facts: false
        tasks:
          - name: Initiating Playbook for event apflap
            ansible.builtin.include_role:
              name: ansible_role_nw_paloalto_contentupgrade_check
