#!/usr/bin/env python3
"""
Bit-flip domain checker - finds bit-flipped domain variants.

Takes a list of domains and generates all possible single-bit flips in both:
1. The TLD portion (checking if resulting TLDs are valid/registrable)
2. The domain name portion (generating all possible character variants)
"""

import sys
import argparse
from typing import Set, List, Tuple


# Comprehensive list of valid TLDs (both gTLDs and ccTLDs)
# Source: IANA root zone database (subset of most common ones)
VALID_TLDS = {
    # gTLDs
    'com', 'net', 'org', 'edu', 'gov', 'mil', 'int', 'info', 'biz', 'name',
    'pro', 'aero', 'coop', 'museum', 'jobs', 'mobi', 'travel', 'tel', 'asia',
    'cat', 'post', 'xxx', 'cloud', 'online', 'site', 'website', 'space',
    'tech', 'store', 'app', 'web', 'blog', 'shop', 'link', 'live', 'news',
    
    # ccTLDs (country codes)
    'ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'ao', 'aq', 'ar', 'as',
    'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh',
    'bi', 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bw', 'by', 'bz', 'ca',
    'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr',
    'cu', 'cv', 'cw', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz',
    'ec', 'ee', 'eg', 'er', 'es', 'et', 'eu', 'fi', 'fj', 'fk', 'fm', 'fo',
    'fr', 'ga', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp',
    'gq', 'gr', 'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht',
    'hu', 'id', 'ie', 'il', 'im', 'in', 'io', 'iq', 'ir', 'is', 'it', 'je',
    'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw',
    'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv',
    'ly', 'ma', 'mc', 'md', 'me', 'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo',
    'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na',
    'nc', 'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz', 'om',
    'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'pr', 'ps', 'pt',
    'pw', 'py', 'qa', 're', 'ro', 'rs', 'ru', 'rw', 'sa', 'sb', 'sc', 'sd',
    'se', 'sg', 'sh', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'ss', 'st',
    'su', 'sv', 'sx', 'sy', 'sz', 'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk',
    'tl', 'tm', 'tn', 'to', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 'uk',
    'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'ws',
    'ye', 'yt', 'za', 'zm', 'zw',
}


def flip_bit(char: str, bit_position: int) -> str:
    """
    Flip a single bit in a character.
    
    Args:
        char: Single character to flip
        bit_position: Which bit to flip (0-7)
        
    Returns:
        Character with the specified bit flipped
    """
    char_code = ord(char)
    flipped_code = char_code ^ (1 << bit_position)
    # Only return printable ASCII characters
    if 32 <= flipped_code <= 126:
        return chr(flipped_code)
    return None


def generate_bitflip_variants(text: str) -> Set[str]:
    """
    Generate all possible single-bit flips for each character in text.
    
    Args:
        text: String to generate variants for (e.g., 'google' or 'com')
        
    Returns:
        Set of bit-flipped variants
    """
    variants = set()
    
    for char_idx, char in enumerate(text):
        for bit_pos in range(8):  # 8 bits per byte
            flipped_char = flip_bit(char, bit_pos)
            if flipped_char and (flipped_char.isalnum() or flipped_char == '-'):
                # Build the flipped variant
                flipped = text[:char_idx] + flipped_char + text[char_idx + 1:]
                flipped = flipped.lower()
                # Valid domain characters: alphanumeric and hyphen
                if all(c.isalnum() or c == '-' for c in flipped):
                    variants.add(flipped)
    
    return variants


def generate_bitflip_tlds(tld: str) -> Set[str]:
    """
    Generate all possible single-bit flips for each character in TLD.
    
    Args:
        tld: Top-level domain (e.g., 'com', 'fi')
        
    Returns:
        Set of bit-flipped TLD variants
    """
    variants = set()
    
    for char_idx, char in enumerate(tld):
        for bit_pos in range(8):  # 8 bits per byte
            flipped_char = flip_bit(char, bit_pos)
            if flipped_char and flipped_char.isalpha():
                # Build the flipped TLD
                flipped_tld = tld[:char_idx] + flipped_char + tld[char_idx + 1:]
                flipped_tld = flipped_tld.lower()
                variants.add(flipped_tld)
    
    return variants


def parse_domain(domain: str) -> Tuple[str, str]:
    """
    Parse domain into base and TLD.
    
    Args:
        domain: Full domain like 'google.com'

    Returns:
        Tuple of (base, tld) like ('google', 'com')
    """
    parts = domain.strip().split('.')
    if len(parts) >= 2:
        tld = parts[-1]
        base = '.'.join(parts[:-1])
        return base, tld
    return domain, ''


def check_bitflip_domains(domains: List[str], show_invalid: bool = False, check_domain_name: bool = True) -> None:
    """
    Check all bit-flipped variants for given domains.
    
    Args:
        domains: List of domain names to check
        show_invalid: If True, also show invalid TLD variants
        check_domain_name: If True, also check bit-flips in the domain name
    """
    print("Bit-Flip Domain Analysis")
    print("=" * 70)
    print()
    
    total_valid_tlds = 0
    total_tld_variants = 0
    total_domain_variants = 0
    
    for domain in domains:
        base, original_tld = parse_domain(domain)
        if not original_tld:
            print(f"Warning: Skipping invalid domain '{domain}'", file=sys.stderr)
            continue
        
        print(f"\n{domain}")
        print("=" * 70)
        
        # ============== TLD BIT-FLIPS ==============
        print(f"\n[1] TLD Bit-Flips (Original TLD: .{original_tld})")
        print("-" * 70)
        
        # Generate all bit-flipped TLD variants
        tld_variants = generate_bitflip_tlds(original_tld)
        
        # Remove the original TLD from variants
        tld_variants.discard(original_tld)
        
        valid_tld_variants = []
        invalid_tld_variants = []
        
        for variant_tld in sorted(tld_variants):
            total_tld_variants += 1
            if variant_tld in VALID_TLDS:
                valid_tld_variants.append(variant_tld)
                total_valid_tlds += 1
            else:
                invalid_tld_variants.append(variant_tld)
        
        # Show valid TLD variants
        if valid_tld_variants:
            print(f"\n  ✓ VALID/REGISTRABLE bit-flipped TLDs ({len(valid_tld_variants)}):")
            for tld in valid_tld_variants:
                full_domain = f"{base}.{tld}"
                print(f"    → {full_domain}")
        else:
            print(f"\n  No valid bit-flipped TLDs found")
        
        # Optionally show invalid TLD variants
        if show_invalid and invalid_tld_variants:
            print(f"\n  ✗ Invalid TLDs ({len(invalid_tld_variants)}):")
            for tld in invalid_tld_variants[:10]:  # Limit to first 10
                print(f"    → .{tld}")
            if len(invalid_tld_variants) > 10:
                print(f"    ... and {len(invalid_tld_variants) - 10} more")
        
        # ============== DOMAIN NAME BIT-FLIPS ==============
        if check_domain_name:
            print(f"\n[2] Domain Name Bit-Flips (Original: {base})")
            print("-" * 70)
            
            # Generate all bit-flipped domain name variants
            domain_variants = generate_bitflip_variants(base)
            
            # Remove the original domain name from variants
            domain_variants.discard(base)
            
            if domain_variants:
                print(f"\n  Bit-flipped domain names ({len(domain_variants)}):")
                # Show all variants, sorted
                for variant in sorted(domain_variants):
                    full_domain = f"{variant}.{original_tld}"
                    print(f"    → {full_domain}")
                total_domain_variants += len(domain_variants)
            else:
                print(f"\n  No bit-flipped domain name variants generated")
    
    print("\n" + "=" * 70)
    print(f"Summary:")
    print(f"  - {total_valid_tlds} valid TLDs found from {total_tld_variants} TLD variants")
    if check_domain_name:
        print(f"  - {total_domain_variants} domain name variants generated")


def main():
    parser = argparse.ArgumentParser(
        description="Find bit-flipped domain variants (TLD and domain name)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s domains.txt
  %(prog)s domains.txt --show-invalid
  %(prog)s domains.txt --tld-only
  echo "example.com" | %(prog)s -
        """
    )
    parser.add_argument(
        'input_file',
        nargs='?',
        default='-',
        help='File containing domains (one per line), or - for stdin'
    )
    parser.add_argument(
        '-i', '--show-invalid',
        action='store_true',
        help='Also show invalid (non-registrable) TLD variants'
    )
    parser.add_argument(
        '-t', '--tld-only',
        action='store_true',
        help='Only check TLD bit-flips, skip domain name bit-flips'
    )
    
    args = parser.parse_args()
    
    # Read domains
    domains = []
    try:
        if args.input_file == '-':
            domains = [line.strip() for line in sys.stdin if line.strip()]
        else:
            with open(args.input_file, 'r') as f:
                domains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)
    
    if not domains:
        print("Error: No domains provided", file=sys.stderr)
        sys.exit(1)
    
    check_bitflip_domains(domains, show_invalid=args.show_invalid, check_domain_name=not args.tld_only)


if __name__ == '__main__':
    main()
