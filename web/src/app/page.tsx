import ScanForm from "@/components/ScanForm";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.hero}>
      <div>
        <h1 className={styles.title}>Welcome to xwa</h1>
        <p className={styles.subtitle}>
          The comprehensive CLI & Web Engine for advanced SEO auditing, Sitemap structure mapping, and passive Security vulnerability assessments.
        </p>
      </div>
      
      <div className={styles.scanContainer}>
        <ScanForm />
      </div>
    </div>
  );
}
