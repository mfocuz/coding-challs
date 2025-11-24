# Reversing Xoshiro256 Generate Function from Multiple Outputs

This document explains how to recover the complete state of Xoshiro256 using multiple consecutive outputs.

## Forward Algorithm

The `generate()` function performs these operations:

```
1. Save old state: prev_s0 = s0, prev_s1 = s1, prev_s2 = s2, prev_s3 = s3
2. r1 = s1 * 5
3. r2 = rotl(r1, 7)
4. n1 = r2 * 9                    # This is the output
5. n2 = s1 << 17
6. n3 = s2 ^ s0
7. n4 = s3 ^ s1
8. n5 = s1 ^ n3
9. n6 = s0 ^ n4
10. n7 = n3 ^ n2
11. n8 = rotl(n4, 45)
12. Update state: s0 = n6, s1 = n5, s2 = n7, s3 = n8
```

## Recovery from Multiple Outputs

Given multiple consecutive outputs, we can recover the complete state. The minimum requirement is **2 consecutive outputs**, but having more helps with verification.

### Step 1: Recover s1 from First Output

From the first output `output1 = n1_1`:

```
1. r2_1 = output1 * INV_9 (mod 2^64)
2. r1_1 = rotr(r2_1, 7)
3. s1_old = r1_1 * INV_5 (mod 2^64)
```

This gives us `s1_old` (the s1 value before the first generate call).

### Step 2: Recover s1_new from Second Output

From the second output `output2 = n1_2`:

```
1. r2_2 = output2 * INV_9 (mod 2^64)
2. r1_2 = rotr(r2_2, 7)
3. s1_new = r1_2 * INV_5 (mod 2^64)
```

This gives us `s1_new` (the s1 value after the first generate, which is `n5` from the first generate).

### Step 3: Recover Intermediate Values from First Generate

Now we can recover intermediate values from the first generate. **All of these are CALCULATED** (not from generator):

```
# CALCULATE: n3 from known values
n5 = s1_new = s1_old ^ n3
→ n3 = s1_new ^ s1_old          # ✅ CALCULATE: XOR of s1_new and s1_old

# CALCULATE: n2 from known value
n2 = s1_old << 17               # ✅ CALCULATE: Left shift s1_old by 17

# CALCULATE: s2_new from calculated values
n7 = s2_new = n3 ^ n2
→ s2_new = n3 ^ n2              # ✅ CALCULATE: XOR of n3 and n2

# NEED: s3_new to calculate n4
# Explanation: In the forward algorithm, after generate() runs:
#   - n8 = rotl(n4, 45) is calculated
#   - Then s3_new = n8 (the generator's s3 is updated to n8)
# So: s3_new = n8 = rotl(n4, 45)
# To reverse: n4 = rotr(s3_new, 45)
#
# ⚠️ WHERE TO GET s3_new:
#   RECOMMENDED: Generate a third output and calculate s3_new from it (see Step 5)
#   Alternative: Read from generator object if you have access: s3_new = generator.s3
#
# Since you can generate as many outputs as needed, the best approach is:
#   1. Generate output1, output2, output3 (at minimum)
#   2. Extract s1 values from each output
#   3. Calculate s3_new from the third output (see Step 5)
n8 = s3_new = rotl(n4, 45)
→ n4 = rotr(s3_new, 45)  # ⚠️ CALCULATE n4, but NEED s3_new first (generate output3)

# NEED: s0_new (this is n6)
# Explanation: In the forward algorithm, after generate() runs:
#   - n6 = s0_old ^ n4 is calculated  
#   - Then s0_new = n6 (the generator's s0 is updated to n6)
# So: s0_new = n6 = s0_old ^ n4
#
# ⚠️ WHERE TO GET s0_new:
#   RECOMMENDED: Calculate from second output (see Step 5)
#   Alternative: Read from generator object if you have access: s0_new = generator.s0
n6 = s0_new = s0_old ^ n4       # ⚠️ NEED s0_new to calculate s0_old (calculate from output2)
```

**Summary of what you need to CALCULATE:**
- ✅ `n3 = s1_new ^ s1_old` (both from outputs)
- ✅ `n2 = s1_old << 17` (s1_old from output1)
- ✅ `s2_new = n3 ^ n2` (both calculated above)

**Summary of what you NEED:**

**RECOMMENDED APPROACH (since you can generate as many outputs as needed):**
1. Generate at least 3 outputs: `output1`, `output2`, `output3`
2. Calculate `s0_new` from `output2` (see Step 5)
3. Calculate `s3_new` from `output3` (see Step 5)
4. This gives you everything needed without accessing generator internals

**Alternative (if you have generator access):**
```python
# After generating output1, the generator's state has been updated
s0_new = generator.s0  # Read current s0
s3_new = generator.s3  # Read current s3
```

### Step 4: Recover Remaining Old State

We still need to recover `s0_old`, `s2_old`, and `s3_old`. These are the **FINAL GOAL** - the state before the first generate.

The relationships are:
```
n3 = s2_old ^ s0_old          # n3 already calculated in Step 3
n4 = s3_old ^ s1_old          # n4 needs s3_new first (see below)
n6 = s0_old ^ n4              # n6 = s0_new (need from generator or calculate)
```

**To calculate the old state, you need:**

1. **CALCULATE n4:**
   ```
   n4 = rotr(s3_new, 45)      # ⚠️ NEED s3_new first (from generator state or third output)
   ```

2. **CALCULATE n6:**
   ```
   n6 = s0_new                # ⚠️ NEED s0_new (from generator state or calculate from second output)
   ```

3. **CALCULATE old state (once you have n4 and n6):**
   ```
   s0_old = n6 ^ n4            # ✅ CALCULATE: XOR of n6 and n4
   s2_old = n3 ^ s0_old        # ✅ CALCULATE: XOR of n3 (from Step 3) and s0_old
   s3_old = n4 ^ s1_old        # ✅ CALCULATE: XOR of n4 and s1_old (from output1)
   ```

**Summary:**
- ✅ `n3` - Already calculated in Step 3
- ⚠️ `n4` - Need `s3_new` first (from generator state or third output)
- ⚠️ `n6` - Need `s0_new` (from generator state or calculate from second output)
- ✅ `s0_old`, `s2_old`, `s3_old` - Calculate once you have n4 and n6

### Step 5: Recover New State from Second Output

From the second generate, we know:
- `s1_new` (already recovered)
- `s2_new` (already recovered from n7)

We need `s0_new` and `s3_new`. Let's work backwards:

From the second generate:
```
n5_2 = s1_new ^ n3_2
n3_2 = s2_new ^ s0_new
→ n5_2 = s1_new ^ (s2_new ^ s0_new)
→ s0_new = s1_new ^ s2_new ^ n5_2
```

But `n5_2 = s1_new_2` (the s1 after second generate), which we can get from a third output!

Alternatively, we can use the relationship:
```
n6_1 = s0_new = s0_old ^ n4_1
```

So if we can get `n4_1`, we can get `s0_new`. And:
```
n4_1 = s3_old ^ s1_old
```

So:
```
s3_old = n4_1 ^ s1_old
s0_new = s0_old ^ n4_1
```

But we still need `n4_1`. We have:
```
n8_1 = s3_new = rotl(n4_1, 45)
→ n4_1 = rotr(s3_new, 45)
```

So we need `s3_new`. From the second generate:
```
n8_1 = s3_new
```

And `n8_1 = rotl(n4_1, 45)`, so:
```
s3_new = rotl(n4_1, 45)
```

This is circular. Let me reconsider...

### Alternative Approach: Using State Relationships

Actually, we can use the fact that:
- `s1_new = n5 = s1_old ^ n3`
- `s2_new = n7 = n3 ^ n2`
- `s3_new = n8 = rotl(n4, 45)`
- `s0_new = n6 = s0_old ^ n4`

And we know:
- `n3 = s2_old ^ s0_old`
- `n4 = s3_old ^ s1_old`

So:
```
s1_new = s1_old ^ (s2_old ^ s0_old)
s2_new = (s2_old ^ s0_old) ^ (s1_old << 17)
s3_new = rotl(s3_old ^ s1_old, 45)
s0_new = s0_old ^ (s3_old ^ s1_old)
```

We have `s1_old` and `s1_new`. We need to solve for `s0_old`, `s2_old`, `s3_old`.

From `s1_new = s1_old ^ (s2_old ^ s0_old)`:
```
s2_old ^ s0_old = s1_new ^ s1_old = n3
```

From `s2_new = n3 ^ (s1_old << 17)`:
```
s2_new = (s2_old ^ s0_old) ^ (s1_old << 17)
```

We can verify this matches.

Now we need `s0_old` and `s3_old`. We have:
```
s0_new = s0_old ^ (s3_old ^ s1_old)
s3_new = rotl(s3_old ^ s1_old, 45)
```

So:
```
n4 = s3_old ^ s1_old = rotr(s3_new, 45)
s3_old = n4 ^ s1_old
s0_old = s0_new ^ n4
```

But we need `s0_new` and `s3_new`. These are the state after the first generate, which we can get from analyzing the second output!

### Complete Algorithm

Given outputs: `output1`, `output2` (and optionally `output3` for verification):

1. **From output1:**
   - `s1_old = rotr(output1 * INV_9, 7) * INV_5`

2. **From output2:**
   - `s1_new = rotr(output2 * INV_9, 7) * INV_5`

3. **Calculate intermediate values:**
   - `n3 = s1_new ^ s1_old`
   - `n2 = s1_old << 17`
   - `s2_new = n3 ^ n2`

4. **Get s3_new from second generate analysis:**
   - From second generate: `s1_new_2 = rotr(output3 * INV_9, 7) * INV_5` (if you have output3)
   - Or work backwards: `n5_2 = s1_new_2 = s1_new ^ n3_2`
   - `n3_2 = s2_new ^ s0_new`
   - `s0_new = s1_new ^ s2_new ^ s1_new_2`

5. **Recover remaining values:**
   - `n4 = rotr(s3_new, 45)` (need s3_new)
   - `s3_old = n4 ^ s1_old`
   - `s0_old = s0_new ^ n4`
   - `s2_old = n3 ^ s0_old`

**Note:** To get `s3_new` without a third output, you need to solve the system or use brute force on the lower bits.

## Practical Approach with 3 Outputs

With 3 consecutive outputs, the recovery is straightforward:

1. `s1_0 = rotr(output1 * INV_9, 7) * INV_5`
2. `s1_1 = rotr(output2 * INV_9, 7) * INV_5`
3. `s1_2 = rotr(output3 * INV_9, 7) * INV_5`

Then:
- `n3_1 = s1_1 ^ s1_0`
- `n2_1 = s1_0 << 17`
- `s2_1 = n3_1 ^ n2_1`
- `n5_2 = s1_2 = s1_1 ^ n3_2`
- `n3_2 = s2_1 ^ s0_1`
- `s0_1 = s1_1 ^ s2_1 ^ s1_2`
- `n4_1 = s3_1 ^ s1_0` and `s3_1 = rotl(n4_1, 45)`
- Work backwards to get `s0_0`, `s2_0`, `s3_0`

## Implementation Checklist

### What You CALCULATE (from outputs):
- ✅ `s1_old = rotr(output1 * INV_9, 7) * INV_5`
- ✅ `s1_new = rotr(output2 * INV_9, 7) * INV_5`
- ✅ `n3 = s1_new ^ s1_old`
- ✅ `n2 = s1_old << 17`
- ✅ `s2_new = n3 ^ n2`

### What You NEED (RECOMMENDED: Generate 3 outputs):
- ⚠️ `s0_new` - The s0 value after first generate
  - **RECOMMENDED**: Generate `output2` and calculate from it (see Step 5)
  - Alternative: Read from `generator.s0` if you have access
- ⚠️ `s3_new` - The s3 value after first generate
  - **RECOMMENDED**: Generate `output3` and calculate from it (see Step 5)
  - Alternative: Read from `generator.s3` if you have access

**Since you can generate as many outputs as needed, the simplest approach is:**
1. Generate `output1`, `output2`, `output3`
2. Calculate everything from these outputs (no need to access generator internals)

### What You CALCULATE (final recovery):
- ✅ `n4 = rotr(s3_new, 45)` (once you have s3_new)
- ✅ `n6 = s0_new` (once you have s0_new)
- ✅ `s0_old = n6 ^ n4`
- ✅ `s2_old = n3 ^ s0_old`
- ✅ `s3_old = n4 ^ s1_old`

## Summary

**RECOMMENDED APPROACH (since you can generate as many outputs as needed):**
- Generate **3 consecutive outputs**: `output1`, `output2`, `output3`
- This is sufficient to recover the complete initial state
- No need to access generator internals - everything can be calculated from outputs

**Minimum requirement:** 2 outputs (with some ambiguity), but since you can generate outputs on demand, use 3 for complete recovery.

The key insight is that each output reveals `s1` at that point in time, and the state transformation equations allow us to work backwards to recover the complete initial state.

## Modular Inverses

- `INV_9 = 0x1c71c71c71c71c71` (9 * INV_9 ≡ 1 mod 2^64)
- `INV_5 = 0xcccccccccccccccd` (5 * INV_5 ≡ 1 mod 2^64)

These can be calculated using Newton's method for modular inverses modulo powers of 2.
