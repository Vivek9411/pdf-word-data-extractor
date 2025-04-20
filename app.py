import streamlit as st
import pandas as pd
import os
import base64
import uuid
from resume_info import extract_resume_data

# Set page config
st.set_page_config(
    page_title="Resume Parser Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stFileUploader > div > div {
        border: 2px dashed #4a90e2;
        border-radius: 10px;
        padding: 30px;
    }
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .resume-table {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: #2c3e50;
    }
    .resume-table table {
        width: 100%;
        border-collapse: collapse;
    }
    .resume-table td, .resume-table th {
        padding: 12px;
        border-bottom: 1px solid #e0e0e0;
        text-align: left;
    }
    .resume-table tr:hover {
        background-color: #f5f5f5;
    }
    .highlight {
        background-color: #e6f7ff;
        color: #2c3e50;
        padding: 2px 5px;
        border-radius: 4px;
    }
    .filename-header {
        color: #4a90e2;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

def display_resume_table(resume_data):
    """Display individual resume data in a styled table"""
    # Generate unique key using filename and UUID
    table_key = f"resume_table_{resume_data.get('filename', '')}_{uuid.uuid4().hex}"
    
    with st.container():
        st.markdown(f"""
        <div class="resume-table">
            <h4 class="filename-header">📄 {resume_data.get('filename', 'Resume')}</h4>
            <table>
                <tr>
                    <th>Field</th>
                    <th>Details</th>
                </tr>
                <tr>
                    <td><strong>👤 Name</strong></td>
                    <td><span class='highlight'>{resume_data.get('name', 'Not found')}</span></td>
                </tr>
                <tr>
                    <td><strong>📱 Phone</strong></td>
                    <td><span class='highlight'>{" ".join([f"<span class='highlight'>{number}</span>" for number in resume_data.get('mobile_number', [])])}</span></td>
                </tr>
                <tr>
                    <td><strong>📧 Email</strong></td>
                    <td><span class='highlight'>{" ".join([f"<span class='highlight'>{email}</span>" for email in resume_data.get('email', [])])}</span></td>
                </tr>
                <tr>
                    <td><strong>🔗 GitHub</strong></td>
                    <td><span class='highlight'>{" ".join([f"<span class='highlight'>{links}</span>" for links in resume_data.get('github_link', [])])}</span></td>
                </tr>
                <tr>
                    <td><strong>💼 LinkedIn</strong></td>
                    <td><span class='highlight'>{" ".join([f"<span class='highlight'>{links}</span>" for links in resume_data.get('linkedin_link', [])])}</span></td>
                </tr>
                <tr>
                    <td><strong>🛠️ Skills</strong></td>
                    <td>{" ".join([f"<span class='highlight'>{skill}</span>" for skill in resume_data.get('skills', [])])}</td>
                </tr>
            </table>
        </div>""", unsafe_allow_html=True)

def create_download_link(df, title="Download CSV"):
    """Generate a download link for the DataFrame"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="resume_data.csv" style="background: linear-gradient(to right, #4a90e2, #5e72e4); color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 8px; font-weight: bold;">{title}</a>'
    return href

def main():
    # Sidebar
    with st.sidebar:
        st.title("Resume Parser Pro")
        st.markdown("""
            Upload multiple resumes (PDF/DOCX) to extract:
            - Contact information
            - Skills
            - GitHub/LinkedIn profiles
        """)
        st.markdown("---")
        st.markdown("### How to use:")
        st.markdown("1. Upload resume files")
        st.markdown("2. View parsed information")
        st.markdown("3. Download as CSV")
        st.markdown("---")

    # Main content
    st.header("📄 Resume Parser Pro")
    st.markdown("Extract valuable information from resumes in seconds!")
    
    # File uploader
    with st.expander("📤 Upload Resumes", expanded=True):
        uploaded_files = st.file_uploader(
            "Drag and drop files here",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

    if uploaded_files:
        results = []
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Process each file
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                status_text.text(f"Processing {i+1}/{len(uploaded_files)}: {uploaded_file.name}")
                progress_bar.progress((i + 1) / len(uploaded_files))
                
                # Save the file temporarily
                file_path = os.path.join("/tmp", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Parse the resume using your function
                file_data = extract_resume_data(file_path)
                
                # Add filename to the data
                file_data["filename"] = uploaded_file.name
                results.append(file_data)
                
                # Remove temporary file
                os.remove(file_path)
                
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                continue

        if results:
            # Clear progress bar
            progress_bar.empty()
            status_text.empty()
            
            # Display individual resume tables
            st.subheader("📋 Parsed Results")
            for resume in results:
                display_resume_table(resume)
                st.markdown("---")
            
            # Convert to DataFrame for table view and download
            df = pd.DataFrame(results)
            
            # Reorder columns for better display
            cols = ['filename', 'name', 'mobile_number', 'email', 
                   'skills', 'github_link', 'linkedin_link']
            
            # Only keep columns that exist in the data
            cols = [col for col in cols if col in df.columns]
            df = df[cols]

            # Convert list columns to comma-separated strings
            def format_column(value):
                if isinstance(value, list):
                    return ', '.join(map(str, value)) if value else ''
                return value

            for column in ['mobile_number', 'email', 'skills', 'github_link', 'linkedin_link']:
                if column in df.columns:
                    df[column] = df[column].apply(format_column)

            # Tabbed view
            tab1, tab2 = st.tabs(["📊 Summary Table", "💾 Download"])
            
            with tab1:
                st.subheader("All Resumes in Table Format")
                st.dataframe(
                    df,
                    use_container_width=True,
                    column_config={
                        "skills": st.column_config.ListColumn(
                            "Skills",
                            help="List of skills found in resume"
                        )
                    }
                )
            
            with tab2:
                st.subheader("Download Options")
                st.markdown("### Download the parsed data as CSV")
                st.markdown(create_download_link(df), unsafe_allow_html=True)
                
                # Show file preview
                st.markdown("### Data Preview")
                st.dataframe(df.head())
        else:
            st.warning("No valid resume data could be extracted from the uploaded files.")

if __name__ == "__main__":
    main()
