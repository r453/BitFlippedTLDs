# Bit-Flipped Domain Checker

A Python security tool that identifies domain variants by analyzing single-bit flips in both:
1. **Top-level domains (TLDs)** - checks if bit-flipped TLDs are valid/registrable
2. **Domain names** - generates all possible bit-flipped character variants

This is useful for typosquatting detection, domain security auditing, and defensive domain registration.

## What is Bit-Flipping?

Bit-flipping attacks exploit the fact that flipping a single bit in a domain can create valid, registrable domains that users might accidentally visit due to:
- Memory corruption
- Network errors
- Hardware faults (Rowhammer attacks)
- Malicious manipulation

**Examples:**
- Flipping bits in `.fi` → `.bi`, `.fk`, `.fm`, `.gi`, `.ni`, or `.vi` (all valid ccTLDs)
- Flipping bits in `google` → `coogle`, `eoogle`, `foogle`, `goggle`, etc.

## Features

- **Comprehensive TLD database**: Includes 200+ gTLDs and ccTLDs
- **Dual analysis mode**: Tests both TLD and domain name bit-flips
- **Bit-flip analysis**: Tests all 8 bits for each character
- **TLD validity checking**: Only reports TLDs that are actually registrable
- **Domain name variants**: Generates all possible character mutations
- **Clean output**: Shows variants with original TLD preserved
- **Multiple formats**: Supports file input or stdin
- **Flexible modes**: Can check TLD-only or full domain analysis

## Requirements

- Python 3.6+
- No external dependencies (uses built-in libraries)

## Installation

```bash
chmod +x bitflip_tld_checker.py
```

## Usage

### Basic Examples

```bash
# Analyze both TLD and domain name (default)
./bitflip_tld_checker.py domains.txt

# Only check TLD bit-flips
./bitflip_tld_checker.py domains.txt --tld-only

# From stdin
echo "example.com" | ./bitflip_tld_checker.py -

# Show both valid and invalid TLD variants
./bitflip_tld_checker.py domains.txt --show-invalid
```

### Input File Format

Create a text file with one domain per line:

```
google.com
example.org
```

### Advanced Usage

```bash
# Save results to file
./bitflip_tld_checker.py domains.txt > bitflip_results.txt

# Process multiple domain lists
cat company1.txt company2.txt | ./bitflip_tld_checker.py -

# Quick check of a single domain
echo "mycompany.com" | ./bitflip_tld_checker.py -
```

### Command-line Options

```bash
./bitflip_tld_checker.py --help
```

**Options:**
- `input_file` - File containing domains (one per line), or `-` for stdin
- `-i, --show-invalid` - Also show invalid (non-registrable) TLD variants
- `-t, --tld-only` - Only check TLD bit-flips, skip domain name analysis

## Output Format

```
Bit-Flip Domain Analysis
======================================================================

google.com
======================================================================

[1] TLD Bit-Flips (Original TLD: .com)
----------------------------------------------------------------------

  No valid bit-flipped TLDs found

[2] Domain Name Bit-Flips (Original: google)
----------------------------------------------------------------------

  Bit-flipped domain names (27):
    → coogle.com
    → eoogle.com
    → foogle.com
    → goggle.com
    ... and 23 more

======================================================================
Summary:
  - 0 valid TLDs found from 13 TLD variants
  - 27 domain name variants generated
```

The analysis is split into two sections:
1. **TLD Bit-Flips**: Shows only valid/registrable TLD variants
2. **Domain Name Bit-Flips**: Shows all character mutations (up to 20 displayed)

## Real-World Use Cases

### 1. Defensive Domain Registration
Identify and register bit-flipped variants of your critical domains to prevent typosquatting:

```bash
./bitflip_tld_checker.py company_domains.txt > variants_to_register.txt
```

### 2. Security Auditing
Check if attackers have registered bit-flipped variants of your domains:

```bash
./bitflip_tld_checker.py domains.txt | grep -v "^  " | while read domain; do
  echo "Checking: $domain"
  whois "$domain" | grep -i "registrar"
done
```

### 3. Brand Protection
Monitor bit-flipped domains for your brand:

```bash
./bitflip_tld_checker.py brand_domains.txt > monitor_list.txt
```

## Example Results

### Common Patterns

**TLDs with many valid bit-flips:**
- `.fi` → 6 valid variants (bi, fk, fm, gi, ni, vi)
- `.se` → 6 valid variants (re, sa, sd, sg, sm, su)
- `.dk` → 5 valid variants (dj, do, fk, lk, tk)

**TLDs with no valid bit-flips:**
- `.com` → 0 valid variants
- `.org` → 0 valid variants
- `.net` → 0 valid variants

**Why some TLDs have no valid variants:**
The letters in `.com`, `.org`, `.net` produce non-existent TLDs when bits are flipped.

## Understanding the Results

The script performs two types of analysis:

### 1. TLD Bit-Flip Analysis
For each domain, the script:
1. Extracts the TLD (e.g., `.fi` from `example.fi`)
2. Flips each of 8 bits in each TLD character
3. Checks if the resulting string is a valid/registrable TLD
4. Reports only valid variants

**Example for `.fi`:**
- Character 'f' (binary: 01100110)
  - Flip bit 0 → 'g' → `.gi` ✓ (valid ccTLD)
  - Flip bit 1 → 'd' → `.di` ✗ (invalid)
  - Flip bit 4 → 'v' → `.vi` ✓ (valid ccTLD)
- Character 'i' (binary: 01101001)
  - Flip bit 3 → 'a' → `.fa` ✗ (invalid)
  - Flip bit 5 → 'k' → `.fk` ✓ (valid ccTLD)

### 2. Domain Name Bit-Flip Analysis
For the domain name portion:
1. Extracts the base name (e.g., `google` from `google.com`)
2. Flips each of 8 bits in each character
3. Generates all possible single-character mutations
4. Keeps the original TLD

**Example for `google`:**
- Character 'g' → can become: c, e, f, w, etc.
- Character 'o' → can become: g, k, m, n, w, etc.
- Results: `coogle.com`, `eoogle.com`, `foogle.com`, `goggle.com`, etc.

All domain name variants are shown (not filtered by registration status).

## Files in This Directory

- `bitflip_tld_checker.py` - Main script
- `domains.txt` - Example domain list
- `README.md` - This file

## Security Considerations

**Why this matters:**
- Attackers can register bit-flipped domains for phishing
- Hardware errors can cause browsers to resolve wrong domains
- Memory corruption can lead users to malicious sites
- Rowhammer attacks can flip bits in memory

**Defensive measures:**
1. Register critical bit-flipped variants
2. Monitor for suspicious registrations
3. Use DNSSEC where possible
4. Implement HSTS for your domains

## Limitations

- Only checks single-bit flips (not multi-bit corruption)
- TLD analysis: Only reports valid/registrable TLDs
- Domain name analysis: Shows all variants (doesn't check availability)
- Requires up-to-date TLD list (script includes 200+ TLDs)
- Does not check actual domain registration status (use `whois` for that)
- Domain name variants limited to alphanumeric and hyphen characters

## Extending the Script

### Add more TLDs
Edit the `VALID_TLDS` set in the script to include additional TLDs from [IANA Root Zone Database](https://www.iana.org/domains/root/db).

### Check domain availability
Combine with `whois`:

```bash
./bitflip_tld_checker.py domains.txt | grep "→" | awk '{print $2}' | while read domain; do
  if whois "$domain" | grep -qi "no match"; then
    echo "Available: $domain"
  fi
done
```

## Further Reading

- [Bit-squatting: DNS Hijacking Without Exploitation](https://dinaburg.org/bitsquatting.html)
- [IANA Root Zone Database](https://www.iana.org/domains/root/db)
- [Rowhammer and DNS Security](https://en.wikipedia.org/wiki/Row_hammer)

## License

MIT License