#!/usr/bin/env python3.12
"""
Test script for document generation functionality.
"""

import sys
from pathlib import Path

print("="*60)
print("Testing Document Generation System")
print("="*60)
print()

# Test 1: Import modules
print("1. Testing module imports...")
try:
    from memov.docgen import (
        CodeAnalyzer,
        GitUtils,
        DocumentGenerator,
        DiagramGenerator,
        DocType,
    )
    print("   ✓ All modules imported successfully")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Initialize components
print("\n2. Testing component initialization...")
try:
    analyzer = CodeAnalyzer(".")
    print("   ✓ CodeAnalyzer initialized")

    git_utils = GitUtils(".")
    print("   ✓ GitUtils initialized")

    generator = DocumentGenerator(analyzer, llm_client=None)
    print("   ✓ DocumentGenerator initialized (fallback mode)")

    diagram_gen = DiagramGenerator(llm_client=None)
    print("   ✓ DiagramGenerator initialized")
except Exception as e:
    print(f"   ✗ Initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Analyze code
print("\n3. Testing code analysis...")
try:
    modules = analyzer.analyze_directory("memov/docgen", extensions=['.py'])
    print(f"   ✓ Analyzed {len(modules)} modules")

    if modules:
        summary = analyzer.generate_summary(modules)
        print(f"   ✓ Generated summary:")
        print(f"      - Total files: {summary['total_files']}")
        print(f"      - Total LOC: {summary['total_loc']}")
        print(f"      - Total functions: {summary['total_functions']}")
        print(f"      - Total classes: {summary['total_classes']}")
except Exception as e:
    print(f"   ✗ Analysis failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Git operations
print("\n4. Testing Git operations...")
try:
    current_branch = git_utils.get_current_branch()
    print(f"   ✓ Current branch: {current_branch}")

    commit_info = git_utils.get_commit_info("HEAD")
    if commit_info:
        print(f"   ✓ Latest commit: {commit_info.hash[:8]}")
        print(f"      Author: {commit_info.author}")
        print(f"      Message: {commit_info.message.split(chr(10))[0][:50]}...")

    changed_files = git_utils.get_changed_files("HEAD", ['.py'])
    print(f"   ✓ Changed files in HEAD: {len(changed_files)}")
except Exception as e:
    print(f"   ✗ Git operations failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Generate diagrams
print("\n5. Testing diagram generation...")
try:
    if modules:
        # Architecture diagram
        arch_diagram = diagram_gen.generate_architecture_diagram(
            modules,
            title="Test Architecture"
        )
        print(f"   ✓ Architecture diagram generated ({len(arch_diagram)} chars)")

        # Class diagram
        all_classes = []
        for module in modules:
            all_classes.extend(module.classes)

        if all_classes:
            class_diagram = diagram_gen.generate_class_diagram(all_classes[:5])
            print(f"   ✓ Class diagram generated ({len(class_diagram)} chars)")
        else:
            print("   - No classes found for class diagram")

        # Dependency graph
        dependencies = analyzer.get_dependencies(modules)
        if dependencies:
            dep_diagram = diagram_gen.generate_dependency_graph(dependencies)
            print(f"   ✓ Dependency diagram generated ({len(dep_diagram)} chars)")
except Exception as e:
    print(f"   ✗ Diagram generation failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Generate documentation (fallback mode)
print("\n6. Testing document generation (fallback mode)...")
try:
    if commit_info and changed_files:
        doc = generator.generate_for_commit(
            commit_hash=commit_info.hash,
            changed_files=changed_files[:5],  # Limit to 5 files
            commit_message=commit_info.message,
            doc_type=DocType.FEATURE
        )
        print(f"   ✓ Document generated:")
        print(f"      Title: {doc.title}")
        print(f"      Length: {len(doc.content)} chars")
        print(f"      Type: {doc.doc_type.value}")

        # Save sample output
        output_dir = Path(".mem/docs/test")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "test_feature.md"

        with open(output_file, 'w') as f:
            f.write(doc.content)

        print(f"   ✓ Sample document saved to: {output_file}")
except Exception as e:
    print(f"   ✗ Document generation failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("✨ All tests completed successfully!")
print("="*60)
print()
print("Next steps:")
print("1. Install CLI dependencies: pip install typer rich")
print("2. Set up LLM API key: export OPENAI_API_KEY='your-key'")
print("3. Install litellm: pip install litellm")
print("4. Run: python3.12 -m memov.docgen_cli --help")
print()
