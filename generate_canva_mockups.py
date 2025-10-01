"""
Generate SavorMe v2.0 Mockups using Canva API
4 Evidence-Based Moods
"""
import asyncio
from app.services.canva_client import canva_client


async def generate_v2_mockups():
    """Generate updated mockups for 4-mood system"""
    
    print("=" * 60)
    print("SavorMe v2.0 Canva Mockup Generator")
    print("4 Evidence-Based Moods")
    print("=" * 60)
    print()
    
    # Check if Canva is configured
    if not canva_client.access_token:
        print("⚠️  Canva API not configured!")
        print()
        print("To use Canva API:")
        print("1. Go to: https://www.canva.com/developers/")
        print("2. Create an app and get credentials")
        print("3. Add to .env file:")
        print("   CANVA_CLIENT_ID=your_client_id")
        print("   CANVA_CLIENT_SECRET=your_client_secret")
        print("   CANVA_ACCESS_TOKEN=your_access_token")
        print()
        print("📝 For now, use the HTML mockups:")
        print("   - mood_selection_v2.html")
        print("   - emotional_rationale_mockup.html")
        return
    
    print("🎨 Creating mood selection screen...")
    design_id = canva_client.create_mood_selection_design_v2()
    
    if design_id:
        print(f"✅ Design created successfully!")
        print(f"   Design ID: {design_id}")
        print(f"   View at: https://www.canva.com/design/{design_id}")
        print()
        
        # Export design
        print("📦 Exporting design...")
        export_url = canva_client.export_design(design_id, format="png")
        
        if export_url:
            print(f"✅ Export ready!")
            print(f"   Download: {export_url}")
        else:
            print("⚠️  Export failed, but design is available in Canva")
    else:
        print("❌ Failed to create design")
    
    print()
    print("=" * 60)
    print("Next steps:")
    print("1. Review design in Canva")
    print("2. Refine colors, spacing, typography")
    print("3. Export high-resolution images")
    print("4. Use as reference for iOS/React development")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(generate_v2_mockups())

