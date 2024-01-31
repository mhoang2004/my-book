def longest_common_subsequence(str1, str2):
    m = len(str1)
    n = len(str2)

    # Create a 2D table to store the lengths of LCS
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Build the dp table in a bottom-up manner
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # The length of LCS is stored in the bottom-right cell of the dp table
    return dp[m][n]
