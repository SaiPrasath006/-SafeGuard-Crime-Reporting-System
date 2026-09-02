import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from app import create_app

def run_tests():
    app = create_app()
    client = app.test_client()

    print("==================================================")
    print("      SAFEGUARD BACKEND & DATABASE TEST SUITE     ")
    print("==================================================")

    # 1. Test Citizen Login (john_doe)
    print("\n[TEST 1] Logging in as Citizen 'john_doe'...")
    res = client.post('/api/auth/login', json={
        "username": "john_doe",
        "password": "user123"
    })
    assert res.status_code == 200, f"Login failed: {res.get_json()}"
    data = res.get_json()
    john_token = data["access_token"]
    user_info = data["user"]
    print(" SUCCESS! Logged in successfully.")
    print(f" User Info: ID={user_info['id']}, Name='{user_info['full_name']}', Email='{user_info['email']}', Phone='{user_info['phone_number']}', Role='{user_info['role']}'")

    # 2. Test Get Profile (/api/auth/me)
    print("\n[TEST 2] Fetching Profile for Logged-In User...")
    res = client.get('/api/auth/me', headers={"Authorization": f"Bearer {john_token}"})
    assert res.status_code == 200, f"Profile fetch failed: {res.get_json()}"
    profile = res.get_json()
    print(" SUCCESS! Profile retrieved:")
    print(f" -> {profile}")

    # 3. Test Fetch Logged In User's Crimes (/api/reports/my-reports)
    print("\n[TEST 3] Fetching Crimes reported by Logged-In User ('john_doe')...")
    res = client.get('/api/reports/my-reports', headers={"Authorization": f"Bearer {john_token}"})
    assert res.status_code == 200, f"My reports fetch failed: {res.get_json()}"
    my_crimes = res.get_json()
    print(f" SUCCESS! Found {len(my_crimes)} crime report(s) submitted by {user_info['full_name']}:")
    for c in my_crimes:
        print(f"   * [{c['tracking_id']}] {c['title']} | Category: {c['category']} | Severity: {c['severity']} | Status: {c['status']}")
        print(f"     Status History Entries: {len(c['status_history'])}")

    # 4. Test Admin Login (admin)
    print("\n[TEST 4] Logging in as Admin 'admin'...")
    res = client.post('/api/auth/login', json={
        "username": "admin",
        "password": "admin123"
    })
    assert res.status_code == 200, f"Admin login failed: {res.get_json()}"
    admin_token = res.get_json()["access_token"]
    print(" SUCCESS! Admin logged in successfully.")

    # 5. Test Admin Listing All Registered Users (/api/admin/users)
    print("\n[TEST 5] Admin Fetching All Registered System Users...")
    res = client.get('/api/admin/users', headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200, f"Users fetch failed: {res.get_json()}"
    all_users = res.get_json()
    print(f" SUCCESS! Retrieved {len(all_users)} registered users:")
    for u in all_users:
        print(f"   * User #{u['id']}: {u['username']} ({u['full_name']}) | Email: {u['email']} | Role: {u['role']} | Reports Filed: {u['total_reports_filed']}")

    # 6. Test Admin Inspecting Specific User Details & Crimes (/api/admin/users/<id>)
    john_id = user_info['id']
    print(f"\n[TEST 6] Admin Inspecting User #{john_id} Details and Complaints...")
    res = client.get(f'/api/admin/users/{john_id}', headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200, f"User details fetch failed: {res.get_json()}"
    user_audit = res.get_json()
    print(f" SUCCESS! Retrieved audit for {user_audit['user_information']['full_name']}:")
    print(f"   User Info: {user_audit['user_information']}")
    print(f"   Crimes Count: {user_audit['total_crimes_count']}")

    # 7. Test Admin Updating Report Status with Comment (/api/admin/reports/<id>/status)
    report_id = my_crimes[0]['id']
    print(f"\n[TEST 7] Admin Updating Status of Report #{report_id} to 'Investigating' with Comment...")
    res = client.put(f'/api/admin/reports/{report_id}/status', 
                     json={
                         "status": "Investigating",
                         "comment": "Cyber Cell investigator assigned to trace transaction IP."
                     },
                     headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200, f"Status update failed: {res.get_json()}"
    updated_report = res.get_json()["report"]
    print(f" SUCCESS! Status updated to '{updated_report['status']}'")
    print(" Status History Logs:")
    for sh in updated_report["status_history"]:
        print(f"   - [{sh['timestamp']}] Status: {sh['status']} | Updated By: {sh['updated_by']} | Comment: '{sh['comment']}'")

    print("\n==================================================")
    print("      ALL BACKEND & DATABASE TESTS PASSED!        ")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
