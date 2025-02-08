for file in .github/workflows/*.yml; do
    awk '/steps:/ {
        print;
        print "      - name: Start Energy Measurement";
        print "        uses: green-coding-solutions/eco-ci-energy-estimation@v4";
        print "        with:";
        print "          task: start-measurement";
        next
    }1' "$file" > temp.yml && mv temp.yml "$file"

    awk '{print} /steps:/ {flag=1; next} flag && /^\s*-/ {
        flag=0;
        print "      - name: Display Energy Results";
        print "        uses: green-coding-solutions/eco-ci-energy-estimation@v4";
        print "        with:";
        print "          task: display-results"
    }' "$file" > temp.yml && mv temp.yml "$file"
done
