import { ProfileUpload } from "@/components/profile/ProfileUpload";

export const metadata = { title: "내 프로필" };

export default function ProfilePage() {
  return (
    <main id="main" className="page-shell py-6">
      <h1 className="sr-only">내 프로필</h1>
      <ProfileUpload />
    </main>
  );
}
